import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { RouterProvider } from 'react-router-dom'
import { router } from './utils/router'
import AuthProvider from 'react-auth-kit/AuthProvider'
import { store } from './utils/authStore'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
  <AuthProvider store={store}>
    <RouterProvider router={router}/>
  </AuthProvider>
  </React.StrictMode>,
)
