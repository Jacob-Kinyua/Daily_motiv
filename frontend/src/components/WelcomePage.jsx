import { CAREER_STAGES } from '../constants.js';

function stageLabel(value) {
  return CAREER_STAGES.find((s) => s.value === value)?.label || value;
}

export default function WelcomePage({ user, onViewRecommendations, onEdit, onUnsubscribe }) {
  const firstName = (user.name || '').split(' ')[0] || user.name;

  return (
    <div className="page">
      <div className="masthead">
        <span className="eyebrow">The Dossier</span>
      </div>

      <div className="tab-wrap">
        <span className="tab">Active File</span>
      </div>
      <div className="card card--filed welcome-card">
        <span className="stamp">{stageLabel(user.career_stage)}</span>
        <h1 className="welcome-greeting">Hello, {firstName}.</h1>
        <p className="welcome-subline">{user.occupation}</p>

        <hr className="welcome-divider" />

        <div className="welcome-body">
          <p><strong>On file as your goal:</strong> {user.career_goals}</p>
          <p style={{ marginTop: 16 }}><strong>What you&rsquo;re reading about:</strong></p>
          <div className="welcome-interests">
            {(user.interests || []).map((tag) => (
              <span className="pill" key={tag}>{tag}</span>
            ))}
          </div>
        </div>

        <div className="action-row">
          <button className="btn btn-primary" onClick={onViewRecommendations}>
            View past recommendations
          </button>
          <button className="btn btn-secondary" onClick={onEdit}>
            Edit my file
          </button>
          <button className="btn btn-danger-outline" onClick={onUnsubscribe}>
            Unsubscribe
          </button>
        </div>
      </div>
    </div>
  );
}
