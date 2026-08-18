import { useState } from 'react';
import { createUser, updateUser } from '../api.js';
import { CAREER_STAGES, INTEREST_TAGS } from '../constants.js';

const emptyForm = {
  name: '',
  email: '',
  occupation: '',
  career_goals: '',
  career_stage: '',
  interests: [],
};

export default function SignupForm({ initialValues, onComplete, onCancelEdit }) {
  const isEditing = Boolean(initialValues);
  const [form, setForm] = useState(
    isEditing
      ? {
          name: initialValues.name || '',
          email: initialValues.email || '',
          occupation: initialValues.occupation || '',
          career_goals: initialValues.career_goals || '',
          career_stage: initialValues.career_stage || '',
          interests: initialValues.interests || [],
        }
      : emptyForm
  );
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: undefined }));
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
    setErrors((prev) => ({ ...prev, interests: undefined }));
  }

  function validate() {
    const next = {};
    if (!form.name.trim()) next.name = 'Tell us who this file belongs to.';
    if (!form.email.trim()) {
      next.email = 'We need an email to send the file to.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) {
      next.email = 'That email address doesn\u2019t look right.';
    }
    if (!form.occupation.trim()) next.occupation = 'What do you do?';
    if (!form.career_goals.trim()) next.career_goals = 'Share at least a line on where you\u2019re headed.';
    if (!form.career_stage) next.career_stage = 'Pick the stage closest to where you are now.';
    if (form.interests.length === 0) next.interests = 'Choose at least one interest.';
    return next;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const validation = validate();
    setErrors(validation);
    if (Object.keys(validation).length > 0) return;

    setSubmitting(true);
    setSubmitError('');
    try {
      const payload = { ...form, name: form.name.trim(), email: form.email.trim() };
      const result = isEditing
        ? await updateUser(initialValues.id, payload)
        : await createUser(payload);
      onComplete(result);
    } catch (err) {
      setSubmitError(err.message || 'Something went wrong filing your record. Try again.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="masthead">
        <span className="eyebrow">The Dossier</span>
        <h1>{isEditing ? 'Update your file' : 'Open a file'}</h1>
        <p>
          {isEditing
            ? 'Adjust the details below — your next dispatch will reflect the change.'
            : 'Tell us where you\u2019re headed. Each week we\u2019ll send a story of someone who\u2019s been there, plus a fact and a lesson worth stealing.'}
        </p>
      </div>

      <div className="tab-wrap">
        <span className="tab">{isEditing ? 'Edit Record' : 'New Record'}</span>
      </div>
      <div className="card card--filed intake-card">
        <form onSubmit={handleSubmit} noValidate>
          <div className="field-row">
            <div className="field">
              <label className="eyebrow" htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                value={form.name}
                onChange={(e) => updateField('name', e.target.value)}
                placeholder="Ada Okafor"
              />
              {errors.name && <p className="form-error">{errors.name}</p>}
            </div>
            <div className="field">
              <label className="eyebrow" htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => updateField('email', e.target.value)}
                placeholder="you@example.com"
                disabled={isEditing}
              />
              {errors.email && <p className="form-error">{errors.email}</p>}
              {isEditing && (
                <p className="field-hint">Email can&rsquo;t be changed here — contact support to update it.</p>
              )}
            </div>
          </div>

          <div className="field">
            <label className="eyebrow" htmlFor="occupation">Occupation</label>
            <input
              id="occupation"
              type="text"
              value={form.occupation}
              onChange={(e) => updateField('occupation', e.target.value)}
              placeholder="Product Designer at a seed-stage startup"
            />
            {errors.occupation && <p className="form-error">{errors.occupation}</p>}
          </div>

          <div className="field">
            <label className="eyebrow" htmlFor="career_goals">Career goals</label>
            <textarea
              id="career_goals"
              value={form.career_goals}
              onChange={(e) => updateField('career_goals', e.target.value)}
              placeholder="What are you working toward over the next few years?"
            />
            {errors.career_goals && <p className="form-error">{errors.career_goals}</p>}
          </div>

          <div className="field">
            <label className="eyebrow">Career stage</label>
            <div className="stage-options" role="radiogroup" aria-label="Career stage">
              {CAREER_STAGES.map((stage) => (
                <button
                  type="button"
                  key={stage.value}
                  role="radio"
                  aria-checked={form.career_stage === stage.value}
                  className={`stage-option${form.career_stage === stage.value ? ' selected' : ''}`}
                  onClick={() => updateField('career_stage', stage.value)}
                >
                  <span className="stage-label">{stage.label}</span>
                  <span className="stage-hint">{stage.hint}</span>
                </button>
              ))}
            </div>
            {errors.career_stage && <p className="form-error">{errors.career_stage}</p>}
          </div>

          <div className="field">
            <label className="eyebrow">Interests</label>
            <div className="tag-grid" role="group" aria-label="Interests">
              {INTEREST_TAGS.map((tag) => {
                const selected = form.interests.includes(tag);
                return (
                  <button
                    type="button"
                    key={tag}
                    className={`tag-chip${selected ? ' selected' : ''}`}
                    aria-pressed={selected}
                    onClick={() => toggleInterest(tag)}
                  >
                    {tag}
                  </button>
                );
              })}
            </div>
            {errors.interests && <p className="form-error">{errors.interests}</p>}
          </div>

          {submitError && <div className="banner-error">{submitError}</div>}

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Filing\u2026' : isEditing ? 'Save changes' : 'Open my file'}
            </button>
            {isEditing && onCancelEdit && (
              <button type="button" className="btn btn-secondary" onClick={onCancelEdit} disabled={submitting}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
