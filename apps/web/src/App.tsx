import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import styles from "./App.module.css";

type Quake = {
  id: string;
  mag: number;
  place: string | null;
  time: string | null;
  url: string | null;
  latitude: number | null;
  longitude: number | null;
  depth_km: number | null;
  sig: number | null;
};

type ApiResponse = {
  meta: { count: number; window: string; minMag: number; generated_at: string };
  items: Quake[];
};

const API_BASE = "http://localhost:8000";

export default function App() {
  const [window, setWindow] = useState<"hour" | "day" | "week">("day");
  const [minMag, setMinMag] = useState<number>(4.5);
  const [limit, setLimit] = useState<number>(50);

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [selected, setSelected] = useState<Quake | null>(null);

  const title = useMemo(() => "QuakeWatch", []);

  async function load(overrides?: Partial<{ window: typeof window; minMag: number; limit: number }>) {
  const w = overrides?.window ?? window;
  const m = overrides?.minMag ?? minMag;
  const l = overrides?.limit ?? limit;

  setLoading(true);
  setError(null);
  try {
    const res = await axios.get<ApiResponse>(`${API_BASE}/quakes`, {
      params: { window: w, minMag: m, limit: l },
    });
    setData(res.data);
  } catch (e: any) {
    setError(e?.message ?? "Failed to load data");
    setData(null);
  } finally {
    setLoading(false);
  }
}

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [window, minMag, limit]);

  return (
    <div className={styles.page}>
      <header className={styles.topbar}>
        <div className={styles.brand}>
          <div className={styles.wordmark}>
            <span className={styles.badge} aria-hidden="true">
              Public Data
            </span>
            <h1 className={styles.title}>{title}</h1>
          </div>
          <p className={styles.subtitle}>
            Global earthquake activity (USGS feed), presented through a validated API layer.
          </p>
        </div>

        <div className={styles.actions}>
          <button
  className={styles.primaryBtn}
  onClick={() => load({ window, minMag, limit })}
  disabled={loading}
>

            {loading ? "Refreshing…" : "Refresh data"}
          </button>
        </div>
      </header>

      <main className={styles.container}>
        <section className={styles.card}>
          <div className={styles.cardHeader}>
            <h2 className={styles.cardTitle}>Filters</h2>
            {data && (
              <div className={styles.metaLine}>
                Showing <b>{data.meta.count}</b> records • generated{" "}
                {new Date(data.meta.generated_at).toLocaleString()}
              </div>
            )}
          </div>

          <div className={styles.filters}>
            <label className={styles.field}>
              <span className={styles.label}>Time window</span>
              <select
                className={styles.control}
                value={window}
                onChange={(e) => setWindow(e.target.value as any)}
              >
                <option value="hour">Past hour</option>
                <option value="day">Past day</option>
                <option value="week">Past week</option>
              </select>
            </label>

            <label className={styles.field}>
              <span className={styles.label}>Minimum magnitude</span>
              <input
              data-testid="minmag-input"
                className={styles.control}
                type="number"
                step="0.1"
                value={minMag}
                onChange={(e) => setMinMag(Number(e.target.value))}
              />
              <span className={styles.hint}>Example: 4.5</span>
            </label>

            <label className={styles.field}>
              <span className={styles.label}>Max results</span>
              <input
                className={styles.control}
                type="number"
                step="1"
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
              />
              <span className={styles.hint}>1–200</span>
            </label>
          </div>
        </section>

        <section className={styles.card}>
          <div className={styles.cardHeader}>
            <h2 className={styles.cardTitle}>Latest events</h2>
            <div className={styles.smallNote}>
              Times displayed in UTC for consistency.
            </div>
          </div>

          {error && (
            <div className={styles.alert} role="alert">
              <div className={styles.alertTitle}>Data load failed</div>
              <div className={styles.alertBody}>{error}</div>
            </div>
          )}

          {!error && loading && (
  <div data-testid="loading" className={styles.loading}>
    Loading…
  </div>
)}


          {!error && !loading && data && data.items.length === 0 && (
            <div data-testid="empty-state" className={styles.emptyState}>
              No results match the current filters.
            </div>
          )}

          {!error && !loading && data && data.items.length > 0 && (
            <div className={styles.tableWrap}>
              <table data-testid="quakes-table" className={styles.table}>
                <thead>
                  <tr>
                    <th>Mag</th>
                    <th>Location</th>
                    <th>Time (UTC)</th>
                    <th>Depth (km)</th>
                    <th className={styles.right}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((q) => (
                    <tr key={q.id} data-testid="quake-row">
                      <td className={styles.magCell}>
                        <span className={styles.magPill}>{q.mag.toFixed(1)}</span>
                      </td>
                      <td className={styles.placeCell}>{q.place ?? "—"}</td>
                      <td className={styles.timeCell}>
                        {q.time ? new Date(q.time).toUTCString() : "—"}
                      </td>
                      <td>{q.depth_km ?? "—"}</td>
                      <td className={styles.right}>
                        <button
                          data-testid="view-details"
                          className={styles.linkBtn}
                          onClick={() => setSelected(q)}
                        >
                          View details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <footer className={styles.footer}>
          <div>
            Source: <b>USGS Earthquake Hazards Program</b>
          </div>
          <div className={styles.footerRight}>
            Built with FastAPI + React • QA automation via Selenium (in progress)
          </div>
        </footer>
      </main>

      {selected && (
        <div
          data-testid="modal-overlay"
          className={styles.modalOverlay}
          onClick={() => setSelected(null)}
        >
          <div
            data-testid="details-modal"
            className={styles.modal}
            role="dialog"
            aria-modal="true"
            aria-label="Earthquake details"
            onClick={(e) => e.stopPropagation()}
          >
            <div className={styles.modalHeader}>
              <div>
                <div className={styles.modalKicker}>Event details</div>
                <h3 className={styles.modalTitle}>
                  M {selected.mag.toFixed(1)} — {selected.place ?? "—"}
                </h3>
              </div>
              <button
                data-testid="close-modal"
                className={styles.secondaryBtn}
                onClick={() => setSelected(null)}
              >
                Close
              </button>
            </div>

            <div className={styles.modalGrid}>
              <div className={styles.kv}>
                <div className={styles.k}>Time (UTC)</div>
                <div className={styles.v}>
                  {selected.time ? new Date(selected.time).toUTCString() : "—"}
                </div>
              </div>

              <div className={styles.kv}>
                <div className={styles.k}>Depth</div>
                <div className={styles.v}>{selected.depth_km ?? "—"} km</div>
              </div>

              <div className={styles.kv}>
                <div className={styles.k}>Coordinates</div>
                <div className={styles.v}>
                  {selected.latitude}, {selected.longitude}
                </div>
              </div>

              <div className={styles.kv}>
                <div className={styles.k}>Significance</div>
                <div className={styles.v}>{selected.sig ?? "—"}</div>
              </div>
            </div>

            {selected.url && (
              <div className={styles.modalFooter}>
                <a
                  className={styles.externalLink}
                  href={selected.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open official record on USGS →
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
