import { useState } from 'react';
import { unsubscribeUser } from '../api.js';

export default function UnsubscribeModal({ user, onCancel, onConfirmed }) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  async function handleConfirm() {
    setSubmitting(true);
    setError('');
    try {
      await unsubscribeUser(user.id);
      onConfirmed();
    } catch (err) {
      setError(err.message || 'Couldn\u2019t unsubscribe you just now. Try again.');
      setSubmitting(false);
    }
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="unsub-title">
      <div className="card modal-card">
        <span className="stamp" style={{ marginBottom: 14 }}>Confirm</span>
        <h2 id="unsub-title">Close your file?</h2>
        <p>
          You&rsquo;ll stop receiving weekly dispatches at <strong>{user.email}</strong>. You can open a
          new file any time.
        </p>
        {error && <div className="banner-error">{error}</div>}
        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onCancel} disabled={submitting}>
            Keep my subscription
          </button>
          <button className="btn btn-danger-outline" onClick={handleConfirm} disabled={submitting}>
            {submitting ? 'Closing\u2026' : 'Unsubscribe'}
          </button>
        </div>
      </div>
    </div>
  );
}
