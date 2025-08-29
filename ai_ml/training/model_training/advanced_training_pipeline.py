"""
Advanced Training Pipeline for Educational AI Models
Addis Ababa AI School Management System

This module provides a comprehensive training pipeline for custom AI models
including hyperparameter optimization, automated training, and model evaluation.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, random_split
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import optuna
import mlflow
import logging
import json
import os
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Configuration for advanced model training."""
    # Model parameters
    model_type: str
    input_size: int
    hidden_sizes: List[int]
    output_size: int
    dropout_rate: float = 0.3
    
    # Training parameters
    batch_size: int = 32
    learning_rate: float = 0.001
    num_epochs: int = 100
    early_stopping_patience: int = 10
    validation_split: float = 0.2
    test_split: float = 0.1
    
    # Optimization parameters
    optimizer: str = 'adam'
    weight_decay: float = 1e-5
    scheduler: str = 'cosine'
    warmup_steps: int = 1000
    
    # Data parameters
    data_path: str = ''
    feature_columns: List[str] = None
    target_column: str = ''
    categorical_columns: List[str] = None
    numerical_columns: List[str] = None
    
    # Advanced parameters
    use_mixed_precision: bool = True
    gradient_clipping: float = 1.0
    label_smoothing: float = 0.1
    focal_loss_alpha: float = 1.0
    focal_loss_gamma: float = 2.0

class EducationalDataset(Dataset):
    """Custom dataset for educational data."""
    
    def __init__(self, features: np.ndarray, targets: np.ndarray, transform=None):
        self.features = torch.FloatTensor(features)
        self.targets = torch.LongTensor(targets)
        self.transform = transform
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        feature = self.features[idx]
        target = self.targets[idx]
        
        if self.transform:
            feature = self.transform(feature)
        
        return feature, target

class DataPreprocessor:
    """Advanced data preprocessing for educational datasets."""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
    def preprocess_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess the educational dataset."""
        logger.info("Starting data preprocessing...")
        
        # Handle missing values
        data = self._handle_missing_values(data)
        
        # Encode categorical variables
        if self.config.categorical_columns:
            data = self._encode_categorical_variables(data)
        
        # Scale numerical variables
        if self.config.numerical_columns:
            data = self._scale_numerical_variables(data)
        
        # Feature engineering
        data = self._engineer_features(data)
        
        # Prepare features and targets
        features = self._prepare_features(data)
        targets = self._prepare_targets(data)
        
        logger.info(f"Preprocessing complete. Features shape: {features.shape}, Targets shape: {targets.shape}")
        return features, targets
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # For numerical columns, fill with median
        if self.config.numerical_columns:
            for col in self.config.numerical_columns:
                if col in data.columns:
                    data[col] = data[col].fillna(data[col].median())
        
        # For categorical columns, fill with mode
        if self.config.categorical_columns:
            for col in self.config.categorical_columns:
                if col in data.columns:
                    data[col] = data[col].fillna(data[col].mode()[0])
        
        return data
    
    def _encode_categorical_variables(self, data: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical variables using label encoding."""
        for col in self.config.categorical_columns:
            if col in data.columns:
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col].astype(str))
                self.label_encoders[col] = le
        
        return data
    
    def _scale_numerical_variables(self, data: pd.DataFrame) -> pd.DataFrame:
        """Scale numerical variables using standardization."""
        numerical_data = data[self.config.numerical_columns]
        scaled_data = self.scaler.fit_transform(numerical_data)
        data[self.config.numerical_columns] = scaled_data
        
        return data
    
    def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional features for educational data."""
        # Add interaction features
        if len(self.config.numerical_columns) >= 2:
            for i, col1 in enumerate(self.config.numerical_columns):
                for col2 in self.config.numerical_columns[i+1:]:
                    if col1 in data.columns and col2 in data.columns:
                        data[f'{col1}_{col2}_interaction'] = data[col1] * data[col2]
        
        # Add polynomial features for important numerical columns
        important_cols = ['study_time', 'attendance_rate', 'previous_grades']
        for col in important_cols:
            if col in data.columns:
                data[f'{col}_squared'] = data[col] ** 2
                data[f'{col}_cubed'] = data[col] ** 3
        
        # Add temporal features if available
        if 'timestamp' in data.columns:
            data['hour_of_day'] = pd.to_datetime(data['timestamp']).dt.hour
            data['day_of_week'] = pd.to_datetime(data['timestamp']).dt.dayofweek
            data['month'] = pd.to_datetime(data['timestamp']).dt.month
        
        return data
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare feature matrix."""
        # Select feature columns
        if self.config.feature_columns:
            feature_cols = [col for col in self.config.feature_columns if col in data.columns]
        else:
            # Exclude target and non-feature columns
            exclude_cols = [self.config.target_column, 'timestamp', 'student_id']
            feature_cols = [col for col in data.columns if col not in exclude_cols]
        
        self.feature_names = feature_cols
        features = data[feature_cols].values
        
        return features
    
    def _prepare_targets(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare target vector."""
        if self.config.target_column in data.columns:
            targets = data[self.config.target_column].values
        else:
            raise ValueError(f"Target column '{self.config.target_column}' not found in dataset")
        
        return targets

class AdvancedTrainer:
    """Advanced trainer with hyperparameter optimization and automated training."""
    
    def __init__(self, config: TrainingConfig, model_factory):
        self.config = config
        self.model_factory = model_factory
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.best_model = None
        self.training_history = []
        
        # Setup MLflow
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        mlflow.set_experiment("educational_ai_training")
        
        logger.info(f"Training on device: {self.device}")
    
    def train_with_hyperparameter_optimization(self, 
                                             train_data: Tuple[np.ndarray, np.ndarray],
                                             n_trials: int = 100) -> Dict[str, Any]:
        """Train model with hyperparameter optimization using Optuna."""
        logger.info(f"Starting hyperparameter optimization with {n_trials} trials...")
        
        def objective(trial):
            # Suggest hyperparameters
            lr = trial.suggest_float('learning_rate', 1e-5, 1e-1, log=True)
            batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128])
            hidden_sizes = trial.suggest_categorical('hidden_sizes', 
                                                   [[128, 64], [256, 128, 64], [512, 256, 128, 64]])
            dropout_rate = trial.suggest_float('dropout_rate', 0.1, 0.5)
            weight_decay = trial.suggest_float('weight_decay', 1e-6, 1e-3, log=True)
            
            # Update config
            trial_config = TrainingConfig(
                model_type=self.config.model_type,
                input_size=self.config.input_size,
                hidden_sizes=hidden_sizes,
                output_size=self.config.output_size,
                dropout_rate=dropout_rate,
                batch_size=batch_size,
                learning_rate=lr,
                weight_decay=weight_decay,
                num_epochs=50  # Shorter training for optimization
            )
            
            # Train model
            try:
                model, metrics = self._train_single_model(train_data, trial_config)
                return metrics['val_accuracy']
            except Exception as e:
                logger.warning(f"Trial failed: {e}")
                return 0.0
        
        # Run optimization
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        # Get best parameters
        best_params = study.best_params
        logger.info(f"Best hyperparameters: {best_params}")
        
        # Update config with best parameters
        self.config.learning_rate = best_params['learning_rate']
        self.config.batch_size = best_params['batch_size']
        self.config.hidden_sizes = best_params['hidden_sizes']
        self.config.dropout_rate = best_params['dropout_rate']
        self.config.weight_decay = best_params['weight_decay']
        
        # Train final model with best parameters
        final_model, final_metrics = self._train_single_model(train_data, self.config)
        
        return {
            'best_params': best_params,
            'best_model': final_model,
            'final_metrics': final_metrics,
            'optimization_history': study.trials_dataframe()
        }
    
    def _train_single_model(self, 
                           train_data: Tuple[np.ndarray, np.ndarray],
                           config: TrainingConfig) -> Tuple[nn.Module, Dict[str, float]]:
        """Train a single model with given configuration."""
        features, targets = train_data
        
        # Split data
        train_features, val_features, train_targets, val_targets = train_test_split(
            features, targets, test_size=config.validation_split, random_state=42, stratify=targets
        )
        
        # Create datasets
        train_dataset = EducationalDataset(train_features, train_targets)
        val_dataset = EducationalDataset(val_features, val_targets)
        
        # Create dataloaders
        train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=config.batch_size, shuffle=False)
        
        # Create model
        model = self._create_model(config)
        model.to(self.device)
        
        # Setup training components
        criterion = self._create_loss_function(config)
        optimizer = self._create_optimizer(model, config)
        scheduler = self._create_scheduler(optimizer, config)
        
        # Training loop
        best_val_accuracy = 0.0
        patience_counter = 0
        training_history = []
        
        for epoch in range(config.num_epochs):
            # Training phase
            train_loss, train_accuracy = self._train_epoch(model, train_loader, criterion, optimizer)
            
            # Validation phase
            val_loss, val_accuracy = self._validate_epoch(model, val_loader, criterion)
            
            # Learning rate scheduling
            if scheduler:
                scheduler.step()
            
            # Record metrics
            epoch_metrics = {
                'epoch': epoch,
                'train_loss': train_loss,
                'train_accuracy': train_accuracy,
                'val_loss': val_loss,
                'val_accuracy': val_accuracy,
                'learning_rate': optimizer.param_groups[0]['lr']
            }
            training_history.append(epoch_metrics)
            
            # Early stopping
            if val_accuracy > best_val_accuracy:
                best_val_accuracy = val_accuracy
                patience_counter = 0
                self.best_model = model.state_dict().copy()
            else:
                patience_counter += 1
                if patience_counter >= config.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Log progress
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}: Train Loss: {train_loss:.4f}, Train Acc: {train_accuracy:.4f}, "
                          f"Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        
        # Load best model
        model.load_state_dict(self.best_model)
        
        # Calculate final metrics
        final_metrics = {
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'best_val_accuracy': best_val_accuracy,
            'final_epoch': epoch,
            'training_history': training_history
        }
        
        return model, final_metrics
    
    def _create_model(self, config: TrainingConfig) -> nn.Module:
        """Create model based on configuration."""
        if config.model_type == 'transformer':
            return self.model_factory.create_educational_transformer(config)
        elif config.model_type == 'performance_predictor':
            return self.model_factory.create_performance_predictor(config)
        elif config.model_type == 'adaptive_learning':
            return self.model_factory.create_adaptive_learning_network(
                config.input_size, config.output_size
            )
        elif config.model_type == 'pattern_recognizer':
            return self.model_factory.create_learning_pattern_recognizer(
                config.input_size, config.output_size
            )
        elif config.model_type == 'emotional_intelligence':
            return self.model_factory.create_emotional_intelligence_network(
                config.input_size, config.output_size, config.hidden_sizes[0]
            )
        else:
            raise ValueError(f"Unknown model type: {config.model_type}")
    
    def _create_loss_function(self, config: TrainingConfig) -> nn.Module:
        """Create loss function based on configuration."""
        if config.output_size == 1:
            return nn.BCEWithLogitsLoss()
        else:
            if config.label_smoothing > 0:
                return nn.CrossEntropyLoss(label_smoothing=config.label_smoothing)
            else:
                return nn.CrossEntropyLoss()
    
    def _create_optimizer(self, model: nn.Module, config: TrainingConfig) -> optim.Optimizer:
        """Create optimizer based on configuration."""
        if config.optimizer.lower() == 'adam':
            return optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
        elif config.optimizer.lower() == 'adamw':
            return optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
        elif config.optimizer.lower() == 'sgd':
            return optim.SGD(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay, momentum=0.9)
        else:
            raise ValueError(f"Unknown optimizer: {config.optimizer}")
    
    def _create_scheduler(self, optimizer: optim.Optimizer, config: TrainingConfig):
        """Create learning rate scheduler based on configuration."""
        if config.scheduler.lower() == 'cosine':
            return optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config.num_epochs)
        elif config.scheduler.lower() == 'step':
            return optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
        elif config.scheduler.lower() == 'exponential':
            return optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
        else:
            return None
    
    def _train_epoch(self, model: nn.Module, train_loader: DataLoader, 
                     criterion: nn.Module, optimizer: optim.Optimizer) -> Tuple[float, float]:
        """Train for one epoch."""
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch_features, batch_targets in train_loader:
            batch_features = batch_features.to(self.device)
            batch_targets = batch_targets.to(self.device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(batch_features)
            
            # Handle different output formats
            if isinstance(outputs, dict):
                # Multi-task learning
                loss = 0
                for key, output in outputs.items():
                    if key in ['difficulty_prediction', 'learning_style', 'emotion_classification']:
                        loss += criterion(output, batch_targets)
                loss = loss / len(outputs)
            else:
                # Single task
                loss = criterion(outputs, batch_targets)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            if self.config.gradient_clipping > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.config.gradient_clipping)
            
            optimizer.step()
            
            # Calculate accuracy
            if isinstance(outputs, dict):
                # Use first output for accuracy calculation
                first_output = list(outputs.values())[0]
                _, predicted = torch.max(first_output.data, 1)
            else:
                _, predicted = torch.max(outputs.data, 1)
            
            total += batch_targets.size(0)
            correct += (predicted == batch_targets).sum().item()
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        accuracy = correct / total
        
        return avg_loss, accuracy
    
    def _validate_epoch(self, model: nn.Module, val_loader: DataLoader, 
                       criterion: nn.Module) -> Tuple[float, float]:
        """Validate for one epoch."""
        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch_features, batch_targets in val_loader:
                batch_features = batch_features.to(self.device)
                batch_targets = batch_targets.to(self.device)
                
                # Forward pass
                outputs = model(batch_features)
                
                # Handle different output formats
                if isinstance(outputs, dict):
                    # Multi-task learning
                    loss = 0
                    for key, output in outputs.items():
                        if key in ['difficulty_prediction', 'learning_style', 'emotion_classification']:
                            loss += criterion(output, batch_targets)
                    loss = loss / len(outputs)
                else:
                    # Single task
                    loss = criterion(outputs, batch_targets)
                
                # Calculate accuracy
                if isinstance(outputs, dict):
                    # Use first output for accuracy calculation
                    first_output = list(outputs.values())[0]
                    _, predicted = torch.max(first_output.data, 1)
                else:
                    _, predicted = torch.max(outputs.data, 1)
                
                total += batch_targets.size(0)
                correct += (predicted == batch_targets).sum().item()
                total_loss += loss.item()
        
        avg_loss = total_loss / len(val_loader)
        accuracy = correct / total
        
        return avg_loss, accuracy

class ModelEvaluator:
    """Advanced model evaluation for educational AI models."""
    
    def __init__(self, model: nn.Module, device: torch.device):
        self.model = model
        self.device = device
        self.model.eval()
    
    def evaluate_model(self, test_loader: DataLoader) -> Dict[str, Any]:
        """Comprehensive model evaluation."""
        logger.info("Starting comprehensive model evaluation...")
        
        all_predictions = []
        all_targets = []
        all_probabilities = []
        
        with torch.no_grad():
            for batch_features, batch_targets in test_loader:
                batch_features = batch_features.to(self.device)
                batch_targets = batch_targets.to(self.device)
                
                # Get predictions
                outputs = self.model(batch_features)
                
                # Handle different output formats
                if isinstance(outputs, dict):
                    # Use first output for evaluation
                    first_output = list(outputs.values())[0]
                    probabilities = torch.softmax(first_output, dim=1)
                    _, predictions = torch.max(first_output, 1)
                else:
                    probabilities = torch.softmax(outputs, dim=1)
                    _, predictions = torch.max(outputs, 1)
                
                all_predictions.extend(predictions.cpu().numpy())
                all_targets.extend(batch_targets.cpu().numpy())
                all_probabilities.extend(probabilities.cpu().numpy())
        
        # Calculate metrics
        metrics = self._calculate_metrics(all_targets, all_predictions, all_probabilities)
        
        # Generate visualizations
        self._generate_evaluation_plots(all_targets, all_predictions, all_probabilities)
        
        return metrics
    
    def _calculate_metrics(self, targets: List, predictions: List, 
                          probabilities: List) -> Dict[str, Any]:
        """Calculate comprehensive evaluation metrics."""
        targets = np.array(targets)
        predictions = np.array(predictions)
        probabilities = np.array(probabilities)
        
        # Basic metrics
        accuracy = accuracy_score(targets, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(targets, predictions, average='weighted')
        
        # Confusion matrix
        cm = confusion_matrix(targets, predictions)
        
        # Per-class metrics
        per_class_precision, per_class_recall, per_class_f1, _ = precision_recall_fscore_support(
            targets, predictions, average=None
        )
        
        # Additional metrics for educational context
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm.tolist(),
            'per_class_precision': per_class_precision.tolist(),
            'per_class_recall': per_class_recall.tolist(),
            'per_class_f1': per_class_f1.tolist(),
            'total_samples': len(targets),
            'class_distribution': np.bincount(targets).tolist()
        }
        
        # Calculate educational-specific metrics
        if len(np.unique(targets)) > 2:  # Multi-class classification
            metrics.update(self._calculate_educational_metrics(targets, predictions, probabilities))
        
        return metrics
    
    def _calculate_educational_metrics(self, targets: np.ndarray, predictions: np.ndarray, 
                                     probabilities: np.ndarray) -> Dict[str, Any]:
        """Calculate metrics specific to educational applications."""
        # Grade prediction accuracy (assuming grades are ordered)
        grade_accuracy = self._calculate_grade_accuracy(targets, predictions)
        
        # Risk assessment accuracy (for students at risk)
        risk_accuracy = self._calculate_risk_accuracy(targets, predictions)
        
        # Confidence calibration
        confidence_metrics = self._calculate_confidence_metrics(targets, probabilities)
        
        return {
            'grade_accuracy': grade_accuracy,
            'risk_accuracy': risk_accuracy,
            'confidence_metrics': confidence_metrics
        }
    
    def _calculate_grade_accuracy(self, targets: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy considering grade proximity."""
        # Define grade proximity weights (closer grades get higher scores)
        grade_weights = np.array([
            [1.0, 0.8, 0.6, 0.4, 0.2],  # A
            [0.8, 1.0, 0.8, 0.6, 0.4],  # B
            [0.6, 0.8, 1.0, 0.8, 0.6],  # C
            [0.4, 0.6, 0.8, 1.0, 0.8],  # D
            [0.2, 0.4, 0.6, 0.8, 1.0]   # F
        ])
        
        weighted_accuracy = 0.0
        for target, pred in zip(targets, predictions):
            weighted_accuracy += grade_weights[target][pred]
        
        return weighted_accuracy / len(targets)
    
    def _calculate_risk_accuracy(self, targets: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy for identifying at-risk students."""
        # Define at-risk grades (D and F)
        at_risk_grades = [3, 4]  # Assuming 0=A, 1=B, 2=C, 3=D, 4=F
        
        at_risk_targets = np.isin(targets, at_risk_grades)
        at_risk_predictions = np.isin(predictions, at_risk_grades)
        
        return accuracy_score(at_risk_targets, at_risk_predictions)
    
    def _calculate_confidence_metrics(self, targets: np.ndarray, probabilities: np.ndarray) -> Dict[str, float]:
        """Calculate confidence calibration metrics."""
        # Get predicted probabilities for correct class
        correct_probs = probabilities[np.arange(len(targets)), targets]
        
        # Calculate confidence metrics
        avg_confidence = np.mean(correct_probs)
        confidence_std = np.std(correct_probs)
        
        # Calculate calibration error (simplified)
        # Group predictions by confidence and calculate accuracy
        confidence_bins = np.linspace(0, 1, 11)
        calibration_errors = []
        
        for i in range(len(confidence_bins) - 1):
            mask = (correct_probs >= confidence_bins[i]) & (correct_probs < confidence_bins[i + 1])
            if np.sum(mask) > 0:
                bin_confidence = np.mean(correct_probs[mask])
                bin_accuracy = np.mean(targets[mask] == np.argmax(probabilities[mask], axis=1))
                calibration_errors.append(abs(bin_confidence - bin_accuracy))
        
        avg_calibration_error = np.mean(calibration_errors) if calibration_errors else 0.0
        
        return {
            'average_confidence': float(avg_confidence),
            'confidence_std': float(confidence_std),
            'calibration_error': float(avg_calibration_error)
        }
    
    def _generate_evaluation_plots(self, targets: List, predictions: List, probabilities: List):
        """Generate evaluation visualization plots."""
        targets = np.array(targets)
        predictions = np.array(predictions)
        probabilities = np.array(probabilities)
        
        # Create plots directory
        os.makedirs('evaluation_plots', exist_ok=True)
        
        # 1. Confusion Matrix
        plt.figure(figsize=(10, 8))
        cm = confusion_matrix(targets, predictions)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('evaluation_plots/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Per-class Metrics
        precision, recall, f1, _ = precision_recall_fscore_support(targets, predictions, average=None)
        classes = [f'Class {i}' for i in range(len(precision))]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Precision, Recall, F1
        x = np.arange(len(classes))
        width = 0.25
        
        ax1.bar(x - width, precision, width, label='Precision', alpha=0.8)
        ax1.bar(x, recall, width, label='Recall', alpha=0.8)
        ax1.bar(x + width, f1, width, label='F1-Score', alpha=0.8)
        
        ax1.set_xlabel('Classes')
        ax1.set_ylabel('Score')
        ax1.set_title('Per-Class Metrics')
        ax1.set_xticks(x)
        ax1.set_xticklabels(classes)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Confidence Distribution
        max_probs = np.max(probabilities, axis=1)
        ax2.hist(max_probs, bins=20, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Prediction Confidence')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Prediction Confidence Distribution')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('evaluation_plots/performance_metrics.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Evaluation plots generated successfully!")

# Example usage
if __name__ == "__main__":
    # Example configuration
    config = TrainingConfig(
        model_type='performance_predictor',
        input_size=50,
        hidden_sizes=[256, 128, 64],
        output_size=5,
        batch_size=32,
        learning_rate=0.001,
        num_epochs=100
    )
    
    # Create trainer
    trainer = AdvancedTrainer(config, None)  # Model factory would be passed here
    
    logger.info("Advanced training pipeline created successfully!")