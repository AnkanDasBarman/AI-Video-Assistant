import "./VideoDetails.css";
import { useParams } from "react-router-dom";
import { useState } from "react";
import api from "../api";

function VideoDetails() {
  const { videoId } = useParams();

  // Core states
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [timeline, setTimeline] = useState([]);
  const [highlights, setHighlights] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [visualQuery, setVisualQuery] = useState("");
  const [visualResults, setVisualResults] = useState([]);

  // UI visibility toggles
  const [showTranscriptSearch, setShowTranscriptSearch] = useState(false);
  const [showVisualSearch, setShowVisualSearch] = useState(false);

  // Loading flags
  const [loading, setLoading] = useState(false); // Ask question
  const [timelineLoading, setTimelineLoading] = useState(false);
  const [highlightsLoading, setHighlightsLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [visualLoading, setVisualLoading] = useState(false);

  const askQuestion = async () => {
    try {
      setLoading(true);
      const res = await api.post("/ask-question", { video_id: videoId, question });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      alert("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  const loadTimeline = async () => {
    try {
      setTimelineLoading(true);
      const res = await api.post("/video-timeline", { video_id: videoId });
      setTimeline(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load timeline");
    } finally {
      setTimelineLoading(false);
    }
  };

  const loadHighlights = async () => {
    try {
      setHighlightsLoading(true);
      const res = await api.post("/video-highlights", { video_id: videoId });
      setHighlights(res.data.highlights);
    } catch (err) {
      console.error(err);
      alert("Failed to load highlights");
    } finally {
      setHighlightsLoading(false);
    }
  };

  const handleTranscriptSearch = async () => {
    try {
      setSearchLoading(true);
      const res = await api.post("/video-search", { video_id: videoId, query: searchQuery });
      const sorted = [...res.data].sort((a, b) => b.score - a.score);
      setSearchResults(sorted);
    } catch (err) {
      console.error(err);
      alert("Failed to search transcript");
    } finally {
      setSearchLoading(false);
    }
  };

  const handleVisualSearch = async () => {
    try {
      setVisualLoading(true);
      const res = await api.post("/visual-search", { video_id: videoId, query: visualQuery });
      setVisualResults(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to search visuals");
    } finally {
      setVisualLoading(false);
    }
  };

  return (
    <div className="video-details-page">
      <section className="video-details-header">
        <h1>Video Details</h1>
        <h2>{videoId}</h2>
      </section>

      {/* Video player */}
      <section className="video-player">
        <video controls style={{ width: '100%', maxHeight: '500px' }}>
          <source src={`http://127.0.0.1:8000/video/${videoId}`} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </section>

      <section className="video-actions">
        <button className="action-btn" onClick={askQuestion} disabled={loading}>
          {loading && <span className="spinner" />}
          Ask Question
        </button>
        <button className="action-btn" onClick={loadTimeline} disabled={timelineLoading}>
          {timelineLoading && <span className="spinner" />}
          Timeline
        </button>
        <button className="action-btn" onClick={loadHighlights} disabled={highlightsLoading}>
          {highlightsLoading && <span className="spinner" />}
          Highlights
        </button>
        <button className="action-btn" onClick={() => setShowTranscriptSearch(!showTranscriptSearch)}>
          Transcript Search
        </button>
        <button className="action-btn" onClick={() => setShowVisualSearch(!showVisualSearch)}>
          Visual Search
        </button>
        

      </section>

      <section className="panel">
        <h3>Question</h3>
        <div className="question-row">
          <input type="text" value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask something..." />
          <button className="action-btn" onClick={askQuestion} disabled={loading}>
            {loading && <span className="spinner" />}
            Ask
          </button>
        </div>
      </section>

      {answer && (
        <section className="panel fade-in">
          <h3>Answer</h3>
          <div className="answer-box">{answer}</div>
        </section>
      )}

      {timeline.length > 0 && (
        <section className="panel fade-in">
          <h3>Timeline</h3>
          {timeline.map((item, i) => (
            <div key={i}><b>{item.start}</b> - {item.topic}</div>
          ))}
        </section>
      )}

      {highlights.length > 0 && (
        <section className="panel fade-in">
          <h3>Highlights</h3>
          {highlights.map((item, i) => (
            <div key={i}>* {item.timestamp} - {item.topic}</div>
          ))}
        </section>
      )}

      {showTranscriptSearch && (
        <section className="panel fade-in">
          <h3>Transcript Search</h3>
          <div className="question-row">
            <input type="text" value={searchQuery} onChange={e => setSearchQuery(e.target.value)} placeholder="Search transcript..." />
            <button className="action-btn" onClick={handleTranscriptSearch} disabled={searchLoading}>
              {searchLoading && <span className="spinner" />}
              Search
            </button>
          </div>
          {searchResults.map((item, i) => (
            <div key={i} className="result-card">
              <strong>{item.start} - {item.end}</strong>
              <p>{item.text}</p>
              <small>Relevance: {(Number(item.score) * 100).toFixed(1)}%</small>
            </div>
          ))}
        </section>
      )}

      {showVisualSearch && (
        <section className="panel fade-in">
          <h3>Visual Search</h3>
          <div className="question-row">
            <input type="text" value={visualQuery} onChange={e => setVisualQuery(e.target.value)} placeholder="Search visual content..." />
            <button className="action-btn" onClick={handleVisualSearch} disabled={visualLoading}>
              {visualLoading && <span className="spinner" />}
              Search
            </button>
          </div>
          {visualResults.map((item, i) => (
            <div key={i} className="result-card">
              <h3>{item.timestamp}</h3>
              <p>{item.caption}</p>
              <small>Relevance: {(Number(item.score) * 100).toFixed(1)}%</small>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

export default VideoDetails;
