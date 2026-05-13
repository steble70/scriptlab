import { useState, useEffect } from "react";

const pythonSkills = [
  { label: "Operativsystem", score: 3, max: 5 },
  { label: "Support", score: 4.5, max: 5 },
  { label: "Molntjänster", score: 3, max: 5 },
  { label: "Programmering", score: 2, max: 5 },
];

const codeSkills = [
  { label: "JSON parsing (json module)", level: "✅ Demonstrated", new: true },
  { label: "os.environ / path handling", level: "✅ Demonstrated", new: true },
  { label: "random.choice() on dicts", level: "✅ Demonstrated", new: true },
  { label: "set() deduplication", level: "✅ Demonstrated", new: true },
  { label: "while / break control flow", level: "✅ Demonstrated", new: true },
  { label: "Args/Returns docstrings", level: "✅ Demonstrated", new: true },
  { label: "__name__ == '__main__' guard", level: "✅ Demonstrated", new: true },
  { label: "**kwargs & functional patterns", level: "✅ Prior work", new: false },
  { label: "OOP / class / generators", level: "✅ Prior work", new: false },
  { label: "matplotlib visualization", level: "✅ Prior work", new: false },
  { label: "JupyterLab + magic commands", level: "✅ Prior work", new: false },
  { label: "pylint / black / pycodestyle", level: "✅ Prior work", new: false },
];

const ai103Topics = [
  { label: "IaaS / PaaS / SaaS concepts", weight: "Core", ready: true, note: "In glossary JSON" },
  { label: "Azure services vocabulary", weight: "Core", ready: true, note: "31 terms in JSON" },
  { label: "Azure Cognitive Services SDK", weight: "Core", ready: false, note: "Not yet coded" },
  { label: "REST API calls (requests)", weight: "Core", ready: false, note: "Not yet coded" },
  { label: "Azure AI Language/Vision/Speech", weight: "Core", ready: false, note: "Not yet coded" },
  { label: "Authentication (Keys, MSI)", weight: "Core", ready: false, note: "Not yet coded" },
  { label: "Azure OpenAI Service", weight: "High", ready: false, note: "Not yet coded" },
  { label: "JSON load/parse/structure", weight: "Medium", ready: true, note: "ccprep.py ✓" },
  { label: "Error handling (try/except)", weight: "Medium", ready: false, note: "Not yet coded" },
  { label: "Azure Monitor / Advisor", weight: "Medium", ready: true, note: "In glossary JSON" },
  { label: "Security & Compliance concepts", weight: "Medium", ready: true, note: "SC-900 certified" },
  { label: "Data viz of AI results", weight: "Good", ready: true, note: "matplotlib ✓" },
  { label: "JupyterLab workflow", weight: "Good", ready: true, note: "Portfolio ✓" },
];

const weightColor = {
  Core: "#FF5252",
  High: "#FF9800",
  Medium: "#FFC107",
  Good: "#4CAF50",
};

const steps = [
  { icon: "🔌", text: "Code a real REST call to Azure AI Language API using requests", priority: "HIGH" },
  { icon: "🔑", text: "Practice authentication: AzureKeyCredential & managed identity", priority: "HIGH" },
  { icon: "🧠", text: "Expand ccprep.py → build an AI-103 quiz (you already have the pattern!)", priority: "MED" },
  { icon: "🛡️", text: "Study Responsible AI principles — exam staple, SC-900 gives you a head start", priority: "MED" },
  { icon: "🧹", text: "Fix pylint E731 (lambda assignment) and E741 (ambiguous 'l') — raise score to 8+", priority: "LOW" },
];

const priorityColor = { HIGH: "#FF5252", MED: "#FF9800", LOW: "#4CAF50" };

const glossarySample = [
  "Cloud Computing", "Azure Functions", "IaaS", "PaaS", "SaaS",
  "Azure Synapse Analytics", "Defense in Depth", "Availability Zone",
];

export default function App() {
  const [tab, setTab] = useState("overview");
  const [animatedScore, setAnimatedScore] = useState(0);
  const [hoveredRow, setHoveredRow] = useState(null);

  const readyCount = ai103Topics.filter(t => t.ready).length;
  const totalCount = ai103Topics.length;
  const readiness = Math.round((readyCount / totalCount) * 100);

  useEffect(() => {
    let frame;
    let current = 0;
    const step = () => {
      current += 1.2;
      if (current >= readiness) { setAnimatedScore(readiness); return; }
      setAnimatedScore(Math.floor(current));
      frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, []);

  const tabs = ["overview", "skills", "gap analysis", "next steps"];

  return (
    <div style={{
      minHeight: "100vh",
      background: "#F5F2EB",
      fontFamily: "'Georgia', serif",
      color: "#1A1A1A",
      padding: "32px 20px",
    }}>
      <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(16px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .card { animation: fadeUp 0.5s ease both; }
        .tab-btn:hover { background: #1A1A1A !important; color: #F5F2EB !important; }
        .row-hover:hover { background: #EDE9E0 !important; }
        .step-card:hover { border-color: #1A1A1A !important; }
      `}</style>

      {/* Header */}
      <div style={{ maxWidth: 860, margin: "0 auto 36px" }}>
        <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
          <div>
            <p style={{ fontSize: 10, letterSpacing: 5, color: "#999", margin: "0 0 6px", textTransform: "uppercase" }}>
              Updated Analysis · v2 · May 2026
            </p>
            <h1 style={{ fontSize: "clamp(32px, 6vw, 58px)", fontWeight: 400, margin: 0, lineHeight: 1, fontStyle: "italic" }}>
              Stefan Blecko
            </h1>
            <p style={{ margin: "6px 0 0", fontSize: 13, letterSpacing: 3, color: "#666", textTransform: "uppercase" }}>
              AI-103 Readiness · Expanded Portfolio
            </p>
          </div>

          {/* Big score */}
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: "clamp(48px, 8vw, 80px)", fontWeight: 900, lineHeight: 1, color: animatedScore >= 55 ? "#2E7D32" : "#E65100", fontFamily: "Georgia, serif" }}>
              {animatedScore}%
            </div>
            <div style={{ fontSize: 11, letterSpacing: 2, color: "#999", textTransform: "uppercase" }}>
              Ready (+{readiness - 30}% from v1)
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ marginTop: 20, background: "#DDD8CF", height: 6, borderRadius: 3, overflow: "hidden" }}>
          <div style={{
            width: `${animatedScore}%`,
            height: "100%",
            background: animatedScore >= 55 ? "#2E7D32" : "#E65100",
            borderRadius: 3,
            transition: "width 0.1s linear",
          }} />
        </div>
      </div>

      {/* Tabs */}
      <div style={{ maxWidth: 860, margin: "0 auto 28px", display: "flex", gap: 8, flexWrap: "wrap" }}>
        {tabs.map(t => (
          <button
            key={t}
            className="tab-btn"
            onClick={() => setTab(t)}
            style={{
              padding: "8px 20px",
              border: "1px solid #1A1A1A",
              borderRadius: 2,
              background: tab === t ? "#1A1A1A" : "transparent",
              color: tab === t ? "#F5F2EB" : "#1A1A1A",
              fontSize: 12,
              letterSpacing: 2,
              textTransform: "uppercase",
              cursor: "pointer",
              fontFamily: "Georgia, serif",
              transition: "all 0.15s",
            }}
          >{t}</button>
        ))}
      </div>

      <div style={{ maxWidth: 860, margin: "0 auto", display: "grid", gap: 20 }}>

        {/* OVERVIEW TAB */}
        {tab === "overview" && <>
          {/* What's new callout */}
          <div className="card" style={{
            background: "#1A1A1A",
            color: "#F5F2EB",
            borderRadius: 4,
            padding: "24px 28px",
            animationDelay: "0s",
          }}>
            <p style={{ fontSize: 10, letterSpacing: 4, color: "#888", margin: "0 0 10px", textTransform: "uppercase" }}>New Evidence — ccprep.py + AZ-900_glossary.json</p>
            <p style={{ margin: 0, fontSize: 15, lineHeight: 1.8, color: "#CCC" }}>
              The new scripts reveal a candidate who is <em style={{ color: "#FFF" }}>actively studying Azure</em> — not just coding for its own sake.
              The glossary quiz tool demonstrates JSON handling, environment variables, randomization logic,
              and professional docstrings. Most importantly, it proves <em style={{ color: "#FFF" }}>Azure vocabulary is being internalized</em> — 
              a real AI-103 differentiator.
            </p>
          </div>

          {/* 3-col stat cards */}
          <div className="card" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, animationDelay: "0.1s" }}>
            {[
              { label: "Azure Terms Known", value: "31", sub: "from JSON glossary", color: "#2E7D32" },
              { label: "Python Concepts", value: "12", sub: "demonstrated in code", color: "#1565C0" },
              { label: "Certifications", value: "2", sub: "MS-900 · SC-900", color: "#6A1B9A" },
              { label: "Pylint Score", value: "7.4", sub: "/ 10  (target: 8+)", color: "#E65100" },
            ].map((s, i) => (
              <div key={i} style={{
                background: "#FFF",
                border: "1px solid #DDD8CF",
                borderRadius: 4,
                padding: "20px 20px 16px",
                borderTop: `3px solid ${s.color}`,
              }}>
                <div style={{ fontSize: 36, fontWeight: 900, color: s.color, lineHeight: 1 }}>{s.value}</div>
                <div style={{ fontSize: 13, fontWeight: 600, margin: "6px 0 2px" }}>{s.label}</div>
                <div style={{ fontSize: 11, color: "#999" }}>{s.sub}</div>
              </div>
            ))}
          </div>

          {/* Glossary cloud */}
          <div className="card" style={{ background: "#FFF", border: "1px solid #DDD8CF", borderRadius: 4, padding: "24px 28px", animationDelay: "0.2s" }}>
            <p style={{ fontSize: 10, letterSpacing: 4, color: "#999", margin: "0 0 16px", textTransform: "uppercase" }}>Azure Glossary Sample (31 terms studied)</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {["Cloud Computing","IaaS","PaaS","SaaS","Azure Functions","Azure OpenAI","ARM Templates",
                "Azure Storage","Azure DevOps","Azure Kubernetes Service","Defense in Depth",
                "Availability Zone","Azure Synapse Analytics","Azure Policy","Compliance Manager",
                "Azure Monitor","Azure Advisor","Azure Active Directory","Azure Firewall",
                "Azure DDoS Protection","Azure Cost Management","SLA","Resource Group",
                "Virtual Machine","Azure Marketplace","Azure App Service","Azure Data Factory",
                "Azure Security Center","Azure Portal","Azure Virtual Network","Subscription"
              ].map(term => (
                <span key={term} style={{
                  background: "#F5F2EB",
                  border: "1px solid #DDD8CF",
                  borderRadius: 2,
                  padding: "4px 10px",
                  fontSize: 11,
                  color: "#444",
                  letterSpacing: 0.3,
                }}>{term}</span>
              ))}
            </div>
          </div>
        </>}

        {/* SKILLS TAB */}
        {tab === "skills" && <>
          <div className="card" style={{ background: "#FFF", border: "1px solid #DDD8CF", borderRadius: 4, padding: "28px", animationDelay: "0s" }}>
            <p style={{ fontSize: 10, letterSpacing: 4, color: "#999", margin: "0 0 20px", textTransform: "uppercase" }}>Portfolio Skill Bars</p>
            {pythonSkills.map(s => (
              <div key={s.label} style={{ marginBottom: 18 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 13 }}>
                  <span>{s.label}</span>
                  <span style={{ fontWeight: 700 }}>{s.score} / {s.max}</span>
                </div>
                <div style={{ background: "#F0EDE6", height: 10, borderRadius: 2 }}>
                  <div style={{ width: `${(s.score / s.max) * 100}%`, height: "100%", background: "#1A1A1A", borderRadius: 2 }} />
                </div>
              </div>
            ))}
          </div>

          <div className="card" style={{ background: "#FFF", border: "1px solid #DDD8CF", borderRadius: 4, padding: "28px", animationDelay: "0.1s" }}>
            <p style={{ fontSize: 10, letterSpacing: 4, color: "#999", margin: "0 0 20px", textTransform: "uppercase" }}>Python Concepts Demonstrated</p>
            <div style={{ display: "grid", gap: 8 }}>
              {codeSkills.map((s, i) => (
                <div key={i} style={{
                  display: "flex", justifyContent: "space-between", alignItems: "center",
                  padding: "10px 14px",
                  background: s.new ? "#F0F7F0" : "#FAFAF8",
                  border: `1px solid ${s.new ? "#A5D6A7" : "#E8E4DC"}`,
                  borderRadius: 3,
                }}>
                  <span style={{ fontSize: 13 }}>{s.label}</span>
                  <span style={{ fontSize: 11, color: s.new ? "#2E7D32" : "#666", fontWeight: s.new ? 700 : 400 }}>
                    {s.level} {s.new && "🆕"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </>}

        {/* GAP ANALYSIS TAB */}
        {tab === "gap analysis" && (
          <div className="card" style={{ background: "#FFF", border: "1px solid #DDD8CF", borderRadius: 4, padding: "28px", animationDelay: "0s" }}>
            <p style={{ fontSize: 10, letterSpacing: 4, color: "#999", margin: "0 0 6px", textTransform: "uppercase" }}>AI-103 Topic Coverage</p>
            <p style={{ fontSize: 12, color: "#AAA", margin: "0 0 20px" }}>{readyCount} of {totalCount} topics covered</p>
            <div style={{ display: "grid", gap: 6 }}>
              {ai103Topics.map((t, i) => (
                <div
                  key={i}
                  className="row-hover"
                  onMouseEnter={() => setHoveredRow(i)}
                  onMouseLeave={() => setHoveredRow(null)}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "24px 1fr auto auto",
                    gap: 12,
                    alignItems: "center",
                    padding: "10px 12px",
                    borderRadius: 3,
                    background: hoveredRow === i ? "#EDE9E0" : "transparent",
                    transition: "background 0.12s",
                    cursor: "default",
                  }}
                >
                  <span style={{ fontSize: 15 }}>{t.ready ? "✅" : "❌"}</span>
                  <span style={{ fontSize: 13, color: t.ready ? "#1A1A1A" : "#999" }}>{t.label}</span>
                  <span style={{ fontSize: 10, color: "#AAA", fontStyle: "italic" }}>{t.note}</span>
                  <span style={{
                    fontSize: 9, fontWeight: 700, letterSpacing: 1,
                    padding: "2px 7px", borderRadius: 2,
                    background: `${weightColor[t.weight]}18`,
                    color: weightColor[t.weight],
                    border: `1px solid ${weightColor[t.weight]}44`,
                    textTransform: "uppercase",
                  }}>{t.weight}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* NEXT STEPS TAB */}
        {tab === "next steps" && (
          <div className="card" style={{ animationDelay: "0s" }}>
            <div style={{ background: "#FFF", border: "1px solid #DDD8CF", borderRadius: 4, padding: "28px", marginBottom: 20 }}>
              <p style={{ fontSize: 10, letterSpacing: 4, color: "#999", margin: "0 0 6px", textTransform: "uppercase" }}>Key Insight</p>
              <p style={{ fontSize: 15, lineHeight: 1.8, margin: 0, color: "#333" }}>
                You already built a <strong>quiz engine</strong> (ccprep.py) that loads JSON, randomizes questions, and deduplicates answers.
                The logical next step is to <strong>replace the static JSON with live Azure AI API calls</strong> — that single upgrade
                would demonstrate most of the remaining core AI-103 skills.
              </p>
            </div>
            <div style={{ display: "grid", gap: 12 }}>
              {steps.map((s, i) => (
                <div
                  key={i}
                  className="step-card"
                  style={{
                    display: "grid",
                    gridTemplateColumns: "48px 1fr auto",
                    gap: 16,
                    alignItems: "center",
                    padding: "18px 20px",
                    background: "#FFF",
                    border: "1px solid #DDD8CF",
                    borderRadius: 4,
                    borderLeft: `4px solid ${priorityColor[s.priority]}`,
                    transition: "border-color 0.15s",
                    cursor: "default",
                  }}
                >
                  <span style={{ fontSize: 26 }}>{s.icon}</span>
                  <span style={{ fontSize: 13, lineHeight: 1.7, color: "#333" }}>{s.text}</span>
                  <span style={{
                    fontSize: 9, fontWeight: 700, letterSpacing: 1.5,
                    color: priorityColor[s.priority],
                    padding: "3px 8px",
                    border: `1px solid ${priorityColor[s.priority]}55`,
                    borderRadius: 2,
                    whiteSpace: "nowrap",
                  }}>{s.priority}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ textAlign: "center", paddingTop: 8, paddingBottom: 24 }}>
          <p style={{ color: "#CCC", fontSize: 10, letterSpacing: 3, textTransform: "uppercase" }}>
            © Stefan Blecko · AI-103 Readiness v2 · Analyzed May 2026
          </p>
        </div>
      </div>
    </div>
  );
}
