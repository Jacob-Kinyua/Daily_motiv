import { useEffect, useState } from 'react';

import SignupForm from './components/SignupForm.jsx';
import LoginPage from './components/LoginPage.jsx';
import WelcomePage from './components/WelcomePage.jsx';
import PastRecommendations from './components/PastRecommendations.jsx';
import UnsubscribeModal from './components/UnsubscribeModal.jsx';

import { getCurrentUser, logout } from './api.js';

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('loading');
  const [showUnsubscribe, setShowUnsubscribe] = useState(false);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    checkSession();
  }, []);

  async function checkSession() {
    try {
      const currentUser = await getCurrentUser();

      setUser(currentUser);
      setView('welcome');
    } catch {
      setUser(null);
      setView('login');
    }
  }

  async function handleLoggedIn() {
    try {
      const currentUser = await getCurrentUser();

      setUser(currentUser);
      setView('welcome');
    } catch {
      setUser(null);
      setView('login');
    }
  }

  function handleUpdated(updatedUser) {
    setUser(updatedUser);
    setEditMode(false);
    setView('welcome');
  }

  async function handleUnsubscribed() {
    await logout();

    setShowUnsubscribe(false);
    setUser(null);
    setView('login');
  }

  async function handleLogout() {
    await logout();

    setUser(null);
    setView('login');
  }

  return (
    <div className="app-shell">

      {view === 'loading' && (
        <div className="loading-screen">
          <p className="eyebrow">Checking your session…</p>
        </div>
      )}

      {view === 'login' && (
        <LoginPage
          onLogin={handleLoggedIn}
          onSignup={() => setView('signup')}
        />
      )}

      {view === 'signup' && (
        <SignupForm
          initialValues={editMode ? user : null}
          onComplete={editMode ? handleUpdated : handleLoggedIn}
          onCancelEdit={
            editMode
              ? () => setView('welcome')
              : () => setView('login')
          }
        />
      )}

      {view === 'welcome' && user && (
        <WelcomePage
          user={user}
          onViewRecommendations={() => setView('recommendations')}
          onEdit={() => {
            setEditMode(true);
            setView('signup');
          }}
          onUnsubscribe={() => setShowUnsubscribe(true)}
          onLogout={handleLogout}
        />
      )}

      {view === 'recommendations' && user && (
        <PastRecommendations
          user={user}
          onBack={() => setView('welcome')}
        />
      )}

      {showUnsubscribe && user && (
        <UnsubscribeModal
          user={user}
          onCancel={() => setShowUnsubscribe(false)}
          onConfirmed={handleUnsubscribed}
        />
      )}

    </div>
  );
}
