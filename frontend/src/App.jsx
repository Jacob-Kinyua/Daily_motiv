import { useEffect, useState } from 'react';
import SignupForm from './components/SignupForm.jsx';
import WelcomePage from './components/WelcomePage.jsx';
import PastRecommendations from './components/PastRecommendations.jsx';
import UnsubscribeModal from './components/UnsubscribeModal.jsx';
import { getUser } from './api.js';

const STORAGE_KEY = 'dossier_user_id';

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('loading'); // loading | signup | welcome | recommendations
  const [showUnsubscribe, setShowUnsubscribe] = useState(false);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    const storedId = localStorage.getItem(STORAGE_KEY);
    if (!storedId) {
      setView('signup');
      return;
    }
    getUser(storedId)
      .then((u) => {
        setUser(u);
        setView('welcome');
      })
      .catch(() => {
        localStorage.removeItem(STORAGE_KEY);
        setView('signup');
      });
  }, []);

  function handleSignedUp(newUser) {
    localStorage.setItem(STORAGE_KEY, newUser.id);
    setUser(newUser);
    setEditMode(false);
    setView('welcome');
  }

  function handleUpdated(updatedUser) {
    setUser(updatedUser);
    setEditMode(false);
    setView('welcome');
  }

  function handleUnsubscribed() {
    localStorage.removeItem(STORAGE_KEY);
    setShowUnsubscribe(false);
    setUser(null);
    setView('signup');
  }

  return (
    <div className="app-shell">
      {view === 'loading' && (
        <div className="loading-screen">
          <p className="eyebrow">Retrieving your file…</p>
        </div>
      )}

      {view === 'signup' && (
        <SignupForm
          initialValues={editMode ? user : null}
          onComplete={editMode ? handleUpdated : handleSignedUp}
          onCancelEdit={editMode ? () => setView('welcome') : null}
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
        />
      )}

      {view === 'recommendations' && user && (
        <PastRecommendations user={user} onBack={() => setView('welcome')} />
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


