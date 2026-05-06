# Git Setup Script for Cloud PC
# Run this on your Cloud PC to set up Git and push to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git Setup for Asset Management System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Configure Git (if not already configured)
Write-Host "Configuring Git..." -ForegroundColor Yellow
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitUser) {
    $userName = Read-Host "Enter your name"
    git config --global user.name "$userName"
    Write-Host "✓ Git user name set to: $userName" -ForegroundColor Green
} else {
    Write-Host "✓ Git user name already set: $gitUser" -ForegroundColor Green
}

if (-not $gitEmail) {
    $userEmail = Read-Host "Enter your email"
    git config --global user.email "$userEmail"
    Write-Host "✓ Git email set to: $userEmail" -ForegroundColor Green
} else {
    Write-Host "✓ Git email already set: $gitEmail" -ForegroundColor Green
}

Write-Host ""

# Initialize Git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path .git) {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

Write-Host ""

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

Write-Host ""

# Commit
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit with PostgreSQL migration and CI/CD setup"
Write-Host "✓ Initial commit created" -ForegroundColor Green

Write-Host ""

# Set main branch
Write-Host "Setting main branch..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Branch set to main" -ForegroundColor Green

Write-Host ""

# Instructions for GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to GitHub: https://github.com/new" -ForegroundColor Yellow
Write-Host "2. Create a new repository (e.g., 'asset-management')" -ForegroundColor Yellow
Write-Host "3. Copy the repository URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Then run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "5. Set up GitHub Secrets (see CICD_SETUP.md)" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Git setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
