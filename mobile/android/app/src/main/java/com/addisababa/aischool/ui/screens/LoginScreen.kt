package com.addisababa.aischool.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.addisababa.aischool.ui.viewmodels.LoginViewModel

@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
    viewModel: LoginViewModel = hiltViewModel()
) {
    val context = LocalContext.current
    val uiState by viewModel.uiState.collectAsState()
    
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var selectedRole by remember { mutableStateOf("admin") }
    
    // Handle login success
    LaunchedEffect(uiState) {
        when (uiState) {
            is LoginUiState.Success -> {
                onLoginSuccess()
            }
            is LoginUiState.Error -> {
                // Error is displayed in the UI
            }
            else -> {}
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "🤖",
            style = MaterialTheme.typography.displayLarge
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Addis Ababa AI School",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = "Revolutionary AI-Powered Education",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.height(48.dp))
        
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            singleLine = true,
            isError = uiState is LoginUiState.Error
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation(),
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Password,
                imeAction = ImeAction.Done
            ),
            singleLine = true,
            isError = uiState is LoginUiState.Error
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Role selector
        ExposedDropdownMenuBox(
            expanded = false,
            onExpandedChange = { },
        ) {
            OutlinedTextField(
                value = selectedRole.replaceFirstChar { it.uppercase() },
                onValueChange = { },
                readOnly = true,
                label = { Text("Role") },
                modifier = Modifier.fillMaxWidth(),
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = false) }
            )
            
            ExposedDropdownMenu(
                expanded = false,
                onDismissRequest = { },
            ) {
                listOf("admin", "teacher", "student", "parent", "staff").forEach { role ->
                    DropdownMenuItem(
                        text = { Text(role.replaceFirstChar { it.uppercase() }) },
                        onClick = { selectedRole = role }
                    )
                }
            }
        }
        
        if (uiState is LoginUiState.Error) {
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = uiState.message,
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall
            )
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Button(
            onClick = {
                if (email.isNotEmpty() && password.isNotEmpty()) {
                    viewModel.login(email, password, selectedRole)
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = uiState !is LoginUiState.Loading && email.isNotEmpty() && password.isNotEmpty()
        ) {
            if (uiState is LoginUiState.Loading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text("Login")
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        TextButton(
            onClick = { /* TODO: Forgot password */ }
        ) {
            Text("Forgot Password?")
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "Demo Credentials: admin@aischool.com / password123",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Connecting to Django Backend",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.primary
        )
    }
}

// UI State for Login
sealed class LoginUiState {
    object Initial : LoginUiState()
    object Loading : LoginUiState()
    object Success : LoginUiState()
    data class Error(val message: String) : LoginUiState()
}