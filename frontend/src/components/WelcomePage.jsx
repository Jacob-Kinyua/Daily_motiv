import { CAREER_STAGES } from '../constants.js';

function stageLabel(value) {
  return CAREER_STAGES.find((s) => s.value === value)?.label || value;
}

export default function WelcomePage({
  user,
  onViewRecommendations,
  onEdit,
  onUnsubscribe,
  onLogout,
}) {
  const firstName =
    (user.name || '').split(' ')[0] || user.name;

  const goals = Array.isArray(user.goals)
    ? user.goals
    : user.goals
      ? [user.goals]
      : [];

  return (
    <div className="page">
      <div className="masthead">
        <span className="eyebrow">The Dossier</span>

        <h1>Hello, {firstName}.</h1>

        <p>
          Your file is active. Here's what we have on record
          and what your upcoming recommendations will be based on.
        </p>
      </div>

      <div className="tab-wrap">
        <span className="tab">Active Record</span>
      </div>

      <div className="card card--filed welcome-card">
        <span className="stamp">
          {stageLabel(user.career_stage)}
        </span>

        <h2 className="welcome-greeting">
          {user.name}
        </h2>

        <p className="welcome-subline">
          {user.occupation}
        </p>

        <hr className="welcome-divider" />

        <div className="welcome-body">

          {/* Career goals */}
          <div className="field">
            <span className="eyebrow">
              Career goals
            </span>

            <div className="welcome-goals">
              {goals.map((goal) => (
                <p key={goal}>{goal}</p>
              ))}
            </div>
          </div>

          {/* Career stage */}
          <div className="field">
            <span className="eyebrow">
              Career stage
            </span>

            <p>{stageLabel(user.career_stage)}</p>
          </div>

          {/* Interests */}
          <div className="field">
            <span className="eyebrow">
              Interests
            </span>

            <div className="welcome-interests">
              {(user.interests || []).map((tag) => (
                <span className="pill" key={tag}>
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button
            className="btn btn-primary"
            onClick={onViewRecommendations}
          >
            View past recommendations
          </button>

          <button
            className="btn btn-secondary"
            onClick={onEdit}
          >
            Edit my file
          </button>

          <button
            className="btn btn-danger-outline"
            onClick={onUnsubscribe}
          >
            Unsubscribe
          </button>

          <button
            className="btn btn-secondary"
            onClick={onLogout}
          >
            Log out
          </button>
        </div>
      </div>
    </div>
  );
}