import { useState } from 'react';
import { createUser, updateUser } from '../api.js';
import { CAREER_STAGES, INTEREST_TAGS } from '../constants.js';

const emptyForm = {
  name: '',
  email: '',
  occupation: '',
  goals: '',
  career_stage: '',
  interests: [],
};

export default function SignupForm({
  initialValues,
  onComplete,
  onCancelEdit,
  onGoToLogin
}) {
  const isEditing = Boolean(initialValues);

  const [form, setForm] = useState(
    isEditing
      ? {
          name: initialValues.name || '',
          email: initialValues.email || '',
          occupation: initialValues.occupation || '',
          goals: Array.isArray(initialValues.goals)
            ? initialValues.goals.join(', ')
            : initialValues.goals || '',
          career_stage: initialValues.career_stage || '',
          interests: initialValues.interests || [],
        }
      : emptyForm
  );

  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function updateField(field, value) {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));

    setErrors((prev) => ({
      ...prev,
      [field]: undefined,
    }));
  }

  function toggleInterest(tag) {
    setForm((prev) => {
      const has = prev.interests.includes(tag);

      return {
        ...prev,
        interests: has
          ? prev.interests.filter((t) => t !== tag)
          : [...prev.interests, tag],
      };
    });

    setErrors((prev) => ({
      ...prev,
      interests: undefined,
    }));
  }

  function validate() {
    const next = {};

    if (!form.name.trim()) {
      next.name = 'Tell us who this file belongs to.';
    }

    if (!form.email.trim()) {
      next.email = 'We need an email to send the file to.';
    } else if (
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())
    ) {
      next.email = 'That email address doesn’t look right.';
    }

    if (!form.occupation.trim()) {
      next.occupation = 'What do you do?';
    }

    if (!form.goals.trim()) {
      next.goals =
        'Share at least a line on where you’re headed.';
    }

    if (!form.career_stage) {
      next.career_stage =
        'Pick the stage closest to where you are now.';
    }

    if (form.interests.length === 0) {
      next.interests = 'Choose at least one interest.';
    }

    return next;
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const validation = validate();

    setErrors(validation);

    if (Object.keys(validation).length > 0) {
      return;
    }

    setSubmitting(true);
    setSubmitError('');

    try {
      const payload = {
        name: form.name.trim(),
        email: form.email.trim(),
        occupation: form.occupation.trim(),

        goals: form.goals
          .split(',')
          .map((goal) => goal.trim())
          .filter(Boolean),

        career_stage: form.career_stage,
        interests: form.interests,
      };

      const result = isEditing
        ? await updateUser(payload)
        : await createUser(payload);

      onComplete(result);

    } catch (err) {
      setSubmitError(
        err.message ||
        'Something went wrong filing your record. Try again.'
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="masthead">
        <span className="eyebrow">The Dossier</span>

        <h1>
          {isEditing ? 'Update your file' : 'Open a file'}
        </h1>

        <p>
          {isEditing
            ? 'Adjust the details below — your next dispatch will reflect the change.'
            : 'Tell us where you’re headed. Each week we’ll send a story of someone who’s been there, plus a fact and a lesson worth stealing.'}
        </p>
      </div>

      <div className="tab-wrap">
        <span className="tab">
          {isEditing ? 'Edit Record' : 'New Record'}
        </span>
      </div>

      <div className="card card--filed intake-card">
        <form onSubmit={handleSubmit} noValidate>

          {/* Name + Email */}
          <div className="field-row">
            <div className="field">
              <label
                className="eyebrow"
                htmlFor="name"
              >
                Name
              </label>

              <input
                id="name"
                type="text"
                value={form.name}
                onChange={(e) =>
                  updateField('name', e.target.value)
                }
                placeholder="Ada Okafor"
              />

              {errors.name && (
                <p className="form-error">
                  {errors.name}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className="eyebrow"
                htmlFor="email"
              >
                Email
              </label>

              <input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) =>
                  updateField('email', e.target.value)
                }
                placeholder="you@example.com"
                disabled={isEditing}
              />

              {errors.email && (
                <p className="form-error">
                  {errors.email}
                </p>
              )}

              {isEditing && (
                <p className="field-hint">
                  Email can’t be changed here — contact
                  support to update it.
                </p>
              )}
            </div>
          </div>

          {/* Occupation */}
          <div className="field">
            <label
              className="eyebrow"
              htmlFor="occupation"
            >
              Occupation
            </label>

            <input
              id="occupation"
              type="text"
              value={form.occupation}
              onChange={(e) =>
                updateField(
                  'occupation',
                  e.target.value
                )
              }
              placeholder="Software Engineer"
            />

            {errors.occupation && (
              <p className="form-error">
                {errors.occupation}
              </p>
            )}
          </div>

          {/* Career goals */}
          <div className="field">
            <label
              className="eyebrow"
              htmlFor="goals"
            >
              Career goals
            </label>

            <textarea
              id="goals"
              value={form.goals}
              onChange={(e) =>
                updateField('goals', e.target.value)
              }
              placeholder="Become a CTO, start an AI company"
            />

            <p className="field-hint">
              Separate multiple goals with commas.
            </p>

            {errors.goals && (
              <p className="form-error">
                {errors.goals}
              </p>
            )}
          </div>

          {/* Career stage */}
          <div className="field">
            <label className="eyebrow">
              Career stage
            </label>

            <div
              className="stage-options"
              role="radiogroup"
              aria-label="Career stage"
            >
              {CAREER_STAGES.map((stage) => (
                <button
                  type="button"
                  key={stage.value}
                  role="radio"
                  aria-checked={
                    form.career_stage === stage.value
                  }
                  className={`stage-option${
                    form.career_stage === stage.value
                      ? ' selected'
                      : ''
                  }`}
                  onClick={() =>
                    updateField(
                      'career_stage',
                      stage.value
                    )
                  }
                >
                  <span className="stage-label">
                    {stage.label}
                  </span>

                  <span className="stage-hint">
                    {stage.hint}
                  </span>
                </button>
              ))}
            </div>

            {errors.career_stage && (
              <p className="form-error">
                {errors.career_stage}
              </p>
            )}
          </div>

          {/* Interests */}
          <div className="field">
            <label className="eyebrow">
              Interests
            </label>

            <div
              className="tag-grid"
              role="group"
              aria-label="Interests"
            >
              {INTEREST_TAGS.map((tag) => {
                const selected =
                  form.interests.includes(tag);

                return (
                  <button
                    type="button"
                    key={tag}
                    className={`tag-chip${
                      selected ? ' selected' : ''
                    }`}
                    aria-pressed={selected}
                    onClick={() =>
                      toggleInterest(tag)
                    }
                  >
                    {tag}
                  </button>
                );
              })}
            </div>

            {errors.interests && (
              <p className="form-error">
                {errors.interests}
              </p>
            )}
          </div>

          {/* Submission error */}
          {submitError && (
            <div className="banner-error">
              {submitError}
            </div>
          )}

          {/* Actions */}
          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting}
            >
              {submitting
                ? 'Filing…'
                : isEditing
                ? 'Save changes'
                : 'Open my file'}
            </button>

            {isEditing && onCancelEdit && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={onCancelEdit}
                disabled={submitting}
              >
                Cancel
              </button>
            )}
          </div>

          {!isEditing && (
            <p className="auth-switch">
              Already have an account?{' '}
              <button
                type="button"
                onClick={onGoToLogin}
                disabled={submitting}
              >
                Log in
              </button>
            </p>
          )}
        </form>
      </div>
    </div>
  );
}