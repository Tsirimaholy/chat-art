#!/usr/bin/env node

/**
 * Development setup script for the chat integration
 * Helps developers check prerequisites and set up the environment
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkFileExists(filePath, description) {
  if (fs.existsSync(filePath)) {
    log(`✅ ${description} exists`, 'green');
    return true;
  } else {
    log(`❌ ${description} missing: ${filePath}`, 'red');
    return false;
  }
}

function checkEnvironmentFile() {
  const envPath = '.env.local';
  if (!fs.existsSync(envPath)) {
    log('📝 Creating .env.local from template...', 'yellow');
    try {
      const template = `# Database
DATABASE_URL="file:./dev.db"

# API URLs  
NEXT_PUBLIC_API_URL="http://localhost:3000"
PYTHON_SERVICE_URL="http://localhost:8001"

# Development settings
NODE_ENV="development"
`;
      fs.writeFileSync(envPath, template);
      log('✅ .env.local created successfully', 'green');
      return true;
    } catch (error) {
      log('❌ Failed to create .env.local', 'red');
      return false;
    }
  } else {
    log('✅ .env.local exists', 'green');
    return true;
  }
}

function checkPythonService() {
  log('\n🐍 Checking Python service connection...', 'blue');
  
  try {
    // Try to connect to Python service
    const { spawn } = require('child_process');
    const curl = spawn('curl', ['-s', '-f', 'http://localhost:8001/chat', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', '{"message":"test"}']);
    
    curl.on('close', (code) => {
      if (code === 0) {
        log('✅ Python service is responding', 'green');
      } else {
        log('⚠️  Python service not available (this is expected during development)', 'yellow');
        log('   Start your Python FastAPI service on port 8001 to enable chat functionality', 'yellow');
      }
    });
  } catch (error) {
    log('⚠️  Could not check Python service (curl not available)', 'yellow');
  }
}

function checkDatabase() {
  log('\n💾 Checking database setup...', 'blue');
  
  try {
    // Check if Prisma client is generated
    if (fs.existsSync('./app/generated/prisma')) {
      log('✅ Prisma client generated', 'green');
    } else {
      log('❌ Prisma client not generated', 'red');
      log('   Run: npm run db:generate', 'yellow');
    }
    
    // Check if database exists
    if (fs.existsSync('./dev.db') || fs.existsSync('./prisma/dev.db')) {
      log('✅ Database file exists', 'green');
    } else {
      log('⚠️  Database file not found', 'yellow');
      log('   Run: npm run db:push && npm run db:seed', 'yellow');
    }
  } catch (error) {
    log('❌ Database check failed', 'red');
  }
}

function main() {
  log('🚀 Chat Integration Development Setup', 'bold');
  log('=====================================\n', 'bold');
  
  // Check core files
  log('📁 Checking core files...', 'blue');
  const coreFiles = [
    ['./components/chat/chat-widget.tsx', 'Chat widget component'],
    ['./components/chat/chat-error-boundary.tsx', 'Chat error boundary'],
    ['./app/api/chat/route.ts', 'Chat API route'],
    ['./lib/chat.ts', 'Chat utilities'],
    ['./types/chat.ts', 'Chat type definitions'],
  ];
  
  let allFilesExist = true;
  coreFiles.forEach(([file, desc]) => {
    if (!checkFileExists(file, desc)) {
      allFilesExist = false;
    }
  });
  
  // Check environment
  log('\n🔧 Checking environment...', 'blue');
  checkEnvironmentFile();
  
  // Check database
  checkDatabase();
  
  // Check Python service
  checkPythonService();
  
  // Summary
  log('\n📋 Setup Summary', 'bold');
  log('================', 'bold');
  
  if (allFilesExist) {
    log('✅ All chat integration files are present', 'green');
  } else {
    log('❌ Some files are missing - check the errors above', 'red');
  }
  
  log('\n🛠️  Next Steps:', 'blue');
  log('1. Start the Next.js development server: npm run dev');
  log('2. Start your Python FastAPI service on port 8001');
  log('3. Visit http://localhost:3000/articles to test the chat widget');
  log('4. Check the browser console and network tab for any errors');
  
  log('\n📚 Useful Commands:', 'blue');
  log('• npm run dev - Start development server');
  log('• npm run db:generate - Generate Prisma client');
  log('• npm run db:push - Push database schema');
  log('• npm run db:seed - Seed database with sample data');
  log('• npm run test - Run tests');
  log('• npm run lint - Check code quality');
  
  log('\n🔗 Documentation:', 'blue');
  log('• README.md - Project overview');
  log('• docs/CHAT_INTEGRATION.md - Chat integration details');
  log('• data/faq-sample.json - Sample FAQ data for Python service');
}

// Handle command line arguments
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  log('Chat Integration Development Setup', 'bold');
  log('Usage: node scripts/dev-setup.js [options]', 'blue');
  log('Options:');
  log('  --help, -h    Show this help message');
  log('  --check-only  Only check files, don\'t create missing ones');
  process.exit(0);
}

// Run the setup
main();