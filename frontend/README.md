# Integrated Ministry Operations Platform - Frontend

React-based frontend for the Integrated Ministry Operations Platform using Tailwind CSS.

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and endpoints
│   ├── components/       # Reusable components
│   ├── pages/           # Page components
│   ├── routes/          # Route guards
│   ├── store/           # State management (Zustand)
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
├── tailwind.config.js   # Tailwind configuration
└── vite.config.js       # Vite configuration
```

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env.local
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:3000`

## Build

```bash
npm run build
```

Production-ready files will be in the `dist` folder.

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Features

- ✅ React 18 with Vite
- ✅ Tailwind CSS for styling
- ✅ React Router for navigation
- ✅ Zustand for state management
- ✅ Axios for API calls
- ✅ JWT authentication
- ✅ Responsive design
- ✅ Dark mode ready (with Tailwind)

## Pages

- **Home** (`/`) - Landing page
- **Login** (`/login`) - User authentication
- **Register** (`/register`) - User registration
- **Dashboard** (`/dashboard`) - Main dashboard (protected)
- **Schools** (`/schools`) - School management
- **Inspections** (`/inspections`) - Inspection management
- **Complaints** (`/complaints`) - Complaint management
- **Resources** (`/resources`) - Resource allocation
- **Field Visits** (`/field-visits`) - Field visit tracking
- **TSC Services** (`/tsc-services`) - TSC service requests

## Components

- **Header** - Navigation header
- **Footer** - Footer component
- **Button** - Reusable button
- **Input** - Form input field
- **Card** - Card container
- **Modal** - Modal dialog
- **Alert** - Alert messages
- **LoadingSpinner** - Loading indicator
- **ProtectedRoute** - Route guard

## State Management

Uses Zustand for authentication state management:

```javascript
import useAuthStore from './store/authStore';

const { user, token, login, logout } = useAuthStore();
```

## API Integration

All API calls go through the centralized API client:

```javascript
import { schoolsAPI, inspectionsAPI } from './api/endpoints';

// Fetch schools
const schools = await schoolsAPI.list();

// Create school
const newSchool = await schoolsAPI.create(data);
```

## Styling with Tailwind CSS

The project uses Tailwind CSS with custom theme configuration:

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: { /* custom primary color */ }
    }
  }
}
```

## Environment Variables

Create `.env.local`:

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## License

MIT
