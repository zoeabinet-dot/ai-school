import SwiftUI
import LocalAuthentication

struct LoginView: View {
    @StateObject private var authService = AuthService()
    @State private var email = ""
    @State private var password = ""
    @State private var isShowingPassword = false
    @State private var isLoading = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var selectedRole: UserRole = .student
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(
                    gradient: Gradient(colors: [Color.blue.opacity(0.8), Color.purple.opacity(0.6)]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 30) {
                        // Header
                        VStack(spacing: 20) {
                            Image(systemName: "graduationcap.fill")
                                .font(.system(size: 80))
                                .foregroundColor(.white)
                            
                            Text("Addis Ababa AI School")
                                .font(.largeTitle)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                            
                            Text("Revolutionary AI-Powered Education")
                                .font(.title3)
                                .foregroundColor(.white.opacity(0.9))
                                .multilineTextAlignment(.center)
                        }
                        .padding(.top, 50)
                        
                        // Login Form
                        VStack(spacing: 20) {
                            // Role Selection
                            Picker("Role", selection: $selectedRole) {
                                ForEach(UserRole.allCases, id: \.self) { role in
                                    Text(role.displayName).tag(role)
                                }
                            }
                            .pickerStyle(SegmentedPickerStyle())
                            .padding(.horizontal)
                            
                            // Email Field
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Email")
                                    .foregroundColor(.white)
                                    .font(.headline)
                                
                                TextField("Enter your email", text: $email)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.emailAddress)
                                    .autocapitalization(.none)
                                    .disableAutocorrection(true)
                            }
                            
                            // Password Field
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Password")
                                    .foregroundColor(.white)
                                    .font(.headline)
                                
                                HStack {
                                    if isShowingPassword {
                                        TextField("Enter your password", text: $password)
                                            .textFieldStyle(RoundedBorderTextFieldStyle())
                                    } else {
                                        SecureField("Enter your password", text: $password)
                                            .textFieldStyle(RoundedBorderTextFieldStyle())
                                    }
                                    
                                    Button(action: {
                                        isShowingPassword.toggle()
                                    }) {
                                        Image(systemName: isShowingPassword ? "eye.slash" : "eye")
                                            .foregroundColor(.gray)
                                    }
                                }
                            }
                            
                            // Login Button
                            Button(action: performLogin) {
                                HStack {
                                    if isLoading {
                                        ProgressView()
                                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                            .scaleEffect(0.8)
                                    } else {
                                        Text("Sign In")
                                            .fontWeight(.semibold)
                                    }
                                }
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                                .background(Color.white)
                                .foregroundColor(.blue)
                                .cornerRadius(25)
                                .shadow(radius: 5)
                            }
                            .disabled(isLoading || email.isEmpty || password.isEmpty)
                            
                            // Biometric Login
                            Button(action: performBiometricLogin) {
                                HStack {
                                    Image(systemName: "faceid")
                                        .font(.title2)
                                    Text("Sign in with Face ID")
                                        .fontWeight(.medium)
                                }
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                                .background(Color.white.opacity(0.2))
                                .foregroundColor(.white)
                                .cornerRadius(25)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 25)
                                        .stroke(Color.white, lineWidth: 1)
                                )
                            }
                            .disabled(isLoading)
                            
                            // Forgot Password
                            Button("Forgot Password?") {
                                // Handle forgot password
                            }
                            .foregroundColor(.white)
                            .font(.subheadline)
                        }
                        .padding(.horizontal, 30)
                        
                        Spacer()
                        
                        // Footer
                        VStack(spacing: 10) {
                            Text("© 2024 Addis Ababa AI School")
                                .foregroundColor(.white.opacity(0.7))
                                .font(.caption)
                            
                            Text("Empowering Education Through AI")
                                .foregroundColor(.white.opacity(0.8))
                                .font(.caption)
                        }
                        .padding(.bottom, 30)
                    }
                }
            }
        }
        .alert("Login Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
        .onAppear {
            checkBiometricAvailability()
        }
    }
    
    private func performLogin() {
        isLoading = true
        
        authService.login(email: email, password: password, role: selectedRole) { result in
            DispatchQueue.main.async {
                isLoading = false
                
                switch result {
                case .success(let user):
                    print("Login successful for user: \(user.email)")
                    // UserManager will handle the authentication state
                case .failure(let error):
                    alertMessage = error.localizedDescription
                    showAlert = true
                }
            }
        }
    }
    
    private func performBiometricLogin() {
        isLoading = true
        
        authService.biometricLogin { result in
            DispatchQueue.main.async {
                isLoading = false
                
                switch result {
                case .success(let user):
                    print("Biometric login successful for user: \(user.email)")
                case .failure(let error):
                    alertMessage = error.localizedDescription
                    showAlert = true
                }
            }
        }
    }
    
    private func checkBiometricAvailability() {
        let context = LAContext()
        var error: NSError?
        
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            print("Biometric authentication available")
        } else {
            print("Biometric authentication not available: \(error?.localizedDescription ?? "Unknown error")")
        }
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
    }
}