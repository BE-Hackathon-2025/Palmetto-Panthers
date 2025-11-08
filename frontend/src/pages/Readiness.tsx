import React, { useState } from "react";
import "@/styles/readiness.css";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function ReadinessForm() {
  const [form, setForm] = useState({
    city_zip: "29201",
    state: "SC",
    language: "en",
    income_net: 4500,
    rent: 1200,
    debts_min: 250,
    savings: 8000,
    dpa_amount: 2000,
    credit_score: 640,
    target_price_min: 180000,
    target_price_max: 220000,
    dp_pct: 3,
    packet_completeness: 50,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const setField = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/readiness/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (err) {
      console.error(err);
      setError(err?.message || "Submission failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="form-shell">
      {/* Top hero/title */}
      <header className="form-hero">
        {/* (Optional) drop in two SVGs/GIFs like your screenshot */}
        {/* <img src="/img/available.svg" alt="" />
        <img src="/img/clock.svg" alt="" /> */}
        <h1 className="form-title">Home Readiness Check</h1>
        <p className="form-subtitle">
          Please fill out the form to estimate your monthly PITI, overall readiness,
          and a realistic timeline to pre-approval.
        </p>
      </header>

      {/* Form card */}
      <form className="form-card" onSubmit={onSubmit}>
        {/* GEO */}
        <div className="grid-2">
          <div className="field">
            <label>ZIP<span className="req">*</span></label>
            <input className="input" value={form.city_zip}
                   onChange={(e)=>setField("city_zip", e.target.value)} />
          </div>
          <div className="field">
            <label>State<span className="req">*</span></label>
            <input className="input" value={form.state}
                   onChange={(e)=>setField("state", e.target.value)} />
          </div>
        </div>

        {/* FINANCIALS */}
        <div className="grid-3">
          <NumberField label="Monthly Net Income ($)" value={form.income_net}
                       onChange={(v)=>setField("income_net", v)} min={0} />
          <NumberField label="Current Rent ($/mo)" value={form.rent}
                       onChange={(v)=>setField("rent", v)} min={0} />
          <NumberField label="Monthly Debts (min $)" value={form.debts_min}
                       onChange={(v)=>setField("debts_min", v)} min={0} />
        </div>

        <div className="grid-3">
          <NumberField label="Savings ($)" value={form.savings}
                       onChange={(v)=>setField("savings", v)} min={0} />
          <NumberField label="DPA Funds ($)" value={form.dpa_amount}
                       onChange={(v)=>setField("dpa_amount", v)} min={0} />
          <NumberField label="Credit Score" value={form.credit_score}
                       onChange={(v)=>setField("credit_score", v)} min={300} max={850} />
        </div>

        {/* GOAL */}
        <div className="grid-3">
          <NumberField label="Target Price Min ($)" value={form.target_price_min}
                       onChange={(v)=>setField("target_price_min", v)} min={0} />
          <NumberField label="Target Price Max ($)" value={form.target_price_max}
                       onChange={(v)=>setField("target_price_max", v)} min={0} />
          <NumberField label="Down Payment (%)" value={form.dp_pct}
                       onChange={(v)=>setField("dp_pct", v)} min={0} step={0.1} />
        </div>

        {/* PROGRESS */}
        <div className="field">
          <label>Packet Completeness: {form.packet_completeness}%</label>
          <input type="range" min={0} max={100} step={1}
                 value={form.packet_completeness}
                 onChange={(e)=>setField("packet_completeness", Number(e.target.value))} />
        </div>

        {error && <div className="error">{error}</div>}

        <div className="cta-row">
          <button className="btn primary" disabled={loading} type="submit">
            {loading ? "Calculating..." : "Check Readiness"}
          </button>
          <button className="btn" type="button" onClick={()=>{ setResult(null); setError(""); }}>
            Reset Result
          </button>
        </div>
      </form>

      {result && <ReadinessResult data={result} />}
    </main>
  );
}

function NumberField({ label, value, onChange, ...rest }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input type="number" className="input" value={value}
             onChange={(e)=>onChange(Number(e.target.value))} {...rest}/>
    </div>
  );
}

/* ------- Result stays the same as your version ------- */
function ReadinessResult({ data }) {
  const {
    score, piti_low, piti_high, eta_weeks,
    affordability_fit, credit_band_points, reserves_months,
    pkt_points, breakdown, timeline,
  } = data;

  const readyNow =
    score >= 70 && affordability_fit >= 60 &&
    credit_band_points >= 60 && reserves_months >= 1;

  const tips = buildRecommendations({
    score, affordability_fit, credit_band_points, reserves_months, pkt_points,
  });

  return (
    <section className="form-card" style={{ marginTop: 24 }}>
      <h2 style={{ marginTop: 0 }}>Your Readiness Results</h2>

      <div className="metrics">
        <div className="metric"><div className="num">{score}</div><div>Overall Score (0–100)</div></div>
        <div className="metric"><div className="num">${piti_low} – ${piti_high}</div><div>Est. PITI / month</div></div>
        <div className="metric"><div className="num">{eta_weeks} weeks</div><div>Estimated ETA</div></div>
      </div>

      <h3 className="section-title">Breakdown</h3>
      <ul className="muted" style={{ lineHeight: 1.8 }}>
        <li>Affordability fit: <strong>{affordability_fit}</strong> (weight {breakdown.affordability.weight}%)</li>
        <li>Credit points: <strong>{credit_band_points}</strong> (weight {breakdown.credit.weight}%)</li>
        <li>Reserves (months): <strong>{Number(reserves_months).toFixed(2)}</strong> (weight {breakdown.reserves.weight}%)</li>
        <li>Packet completeness: <strong>{pkt_points}</strong> (weight {breakdown.packet.weight}%)</li>
      </ul>

      <h3 className="section-title">Recommendations</h3>
      <ul style={{ marginTop: 8 }}>
        {tips.map((t, i) => <li key={i}>{t}</li>)}
      </ul>

      <h3 className="section-title" style={{ marginTop: 18 }}>Timeline</h3>
      <ol className="muted" style={{ lineHeight: 1.8 }}>
        {timeline.map((m) => (
          <li key={m.id}>
            <strong>{m.title}</strong> — week {m.weeks} <em>({m.status})</em>
          </li>
        ))}
      </ol>

      <div className="cta-row">
        {readyNow ? (
          <a className="btn primary" href="/realtors">Connect me to a Realtor</a>
        ) : (
          <a className="btn" href="/resources">See resources to improve readiness</a>
        )}
        <a className="btn" href="/knowledge-center">Learn how readiness is calculated</a>
      </div>
    </section>
  );
}

function buildRecommendations({ score, affordability_fit, credit_band_points, reserves_months, pkt_points }) {
  const tips = [];
  if (credit_band_points < 60) tips.push("Boost credit score: pay on-time, reduce utilization <30%, and avoid new hard pulls for 6–8 weeks.");
  if (affordability_fit < 60) tips.push("Tweak budget/target price: lower target price or increase down payment to fit 28–38% DTI window.");
  if (reserves_months < 2) tips.push("Build reserves: aim for 2 months of PITI from savings/DPA to strengthen your pre-approval.");
  if (pkt_points < 80) tips.push("Complete lender packet: upload paystubs, W-2/1099, bank statements, and ID.");
  if (score >= 80) tips.push("You look strong! Consider locking pre-approval and shopping with a partner agent.");
  return tips.length ? tips : ["Looks good—proceed to connect with a partner agent."];
}
