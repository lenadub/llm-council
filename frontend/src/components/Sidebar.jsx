import { useState, useEffect } from 'react';
import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) {
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch('http://localhost:8001/api/health/workers');
        const data = await res.json();
        setWorkers(data);
      } catch (err) {
        console.error('Failed to fetch worker health:', err);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>LLM Council</h1>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Conversation
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">No conversations yet</div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title">
                {conv.title || 'New Conversation'}
              </div>
              <div className="conversation-meta">
                {conv.message_count} messages
              </div>
            </div>
          ))
        )}
      </div>

      {/* Model health */}
      <div className="model-health">
        <h3>Model Status</h3>

        {workers.length === 0 && (
          <div className="model-health-item">No data</div>
        )}

        {workers.map((worker) => (
          <div key={worker.name} className="model-health-item">
            <span className="model-name">{worker.name}</span>

            {worker.status === 'ok' ? (
              <span className="model-ok">
                ● {worker.latency_ms} ms
              </span>
            ) : (
              <span className="model-offline">
                ● offline
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}