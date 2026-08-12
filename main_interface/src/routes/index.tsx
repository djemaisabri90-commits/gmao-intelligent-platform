import { createBrowserRouter, Navigate } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';          // doit contenir la Navbar + Outlet
import { AuthLayout } from '../layouts/AuthLayout';          // optionnel, pour le login (simple centrage)
import { ProtectedRoute } from '../features/auth/components/ProtectedRoute';
import { LoginPage } from '../features/auth/pages/LoginPage';
import { WorkOrdersPage } from '../features/workorders/pages/WorkOrdersPage';
import { MachinesPage } from '@/features/machines/pages/MachinePage';
import { InterventionsPage } from '@/features/interventions/pages/InterventionsPage';
import { SignalementsPage } from '../features/signalements/pages/SignalementsPage';
import { UsersPage } from '../features/users/pages/UsersPage';
import { AuditLogsPage } from '../features/auditlogs/pages/AuditLogsPage';
import PiecesPage from '../features/pieces/pages/PiecesPage';
import { LogsPage } from '../features/logs/pages/LogsPage';
import { ReportsPage } from '../features/reports/pages/ReportsPage';
import { ResetPasswordPage } from '@/features/auth/pages/ResetPassword';
import { PredictiveDashboard } from '@/features/predictive/pages/predictiveDashboard';
import { LogDetailsPage } from '@/features/predictive/pages/LogDetailsPage';
import { RoleRoute } from '@/features/auth/components/RoleRoute';
import { ForgotPasswordPage } from '@/features/auth/pages/Forgot-password';
import { PasswordResetRequestsPage } from '@/features/requests/pages/PasswordResetRequestsPage';


export const router = createBrowserRouter([
  {
    path: '/',
    element: <ProtectedRoute><MainLayout /></ProtectedRoute>,
    children: [
      {
        index: true,
        element: (() => {
          const user = JSON.parse(localStorage.getItem("auth-storage") || "{}")?.state?.user;

          if (
            user?.role === "operateur" ||
            user?.role === "technicien"
          ) {
            return <Navigate to="/signalements" replace />;
          }

          return <Navigate to="/reports" replace />;
        })(),
      },               // redirection par défaut
      { path: 'workorders', element: <WorkOrdersPage /> },
      { path: 'machines', element: <MachinesPage /> },
      { path: 'interventions', element: <InterventionsPage /> },
      { path: 'signalements', element: <SignalementsPage /> },
      { path: 'utilisateurs',
        element: (
          <RoleRoute allowedRoles={['admin']}>
            <UsersPage />
          </RoleRoute>
        )
      },
      { path: 'auditlogs', element: <AuditLogsPage /> },
      /*{ path: 'auditlogs',
        element: (
          <RoleRoute allowedRoles={['admin']}>
            <AuditLogsPage />
          </RoleRoute>
          )
      },*/
      { path: 'pieces', element: <PiecesPage /> },
      { path: 'logs',
        element: (
          <RoleRoute allowedRoles={['admin', 'expert']}>
            <LogsPage />
          </RoleRoute>
        )
      },
      { path: 'reports',
        element: (
          <RoleRoute allowedRoles={['admin', 'expert']}>
            <ReportsPage />
          </RoleRoute>
        ),          
      },
      { path: 'predictive',
        element: <PredictiveDashboard />
      },
      /* protected route 
      { path: 'predictive',
        element: (
          <RoleRoute allowedRoles={['admin', 'expert']}>
            <PredictiveDashboard />
          </RoleRoute>
        ),
      },*/
      
      { path: 'predictive/train-history/:version',
        element: (
          <RoleRoute allowedRoles={['admin', 'expert']}>
            <LogDetailsPage />
          </RoleRoute>
        )
      },
      
      {path: '/password-reset-requests', element: <PasswordResetRequestsPage /> },

    ],
  },
  {
    path: '/login',
    element: <AuthLayout />,
    children: [{ index: true, element: <LoginPage /> }],
  },
  {
    path: '/reset-password',
    element: <AuthLayout />,
    children: [{ index: true, element: <ResetPasswordPage /> }],
  },
  {
    path: '/password-reset-request',
    element: <AuthLayout />,
    children: [{ index: true, element: <ForgotPasswordPage /> }],
  },
  

]);