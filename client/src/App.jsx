import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Send, Upload, BookOpen, ChevronDown, ChevronUp, FileText, Sparkles, CheckCircle2, AlertCircle, Loader2, Trash2, MessageSquare } from 'lucide-react'
import './index.css'

// Source Display Component
const SourceDisplay = ({ sources }) => {
  const [isOpen, setIsOpen] = useState(false)

  if (!sources || sources.length === 0) return null

  return (
    <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid rgba(75, 85, 99, 0.5)' }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '0.875rem',
          color: '#9ca3af',
          background: 'transparent',
          border: 'none',
          cursor: 'pointer',
          padding: '4px 0',
          transition: 'color 0.2s'
        }}
        onMouseEnter={(e) => e.currentTarget.style.color = '#d1d5db'}
        onMouseLeave={(e) => e.currentTarget.style.color = '#9ca3af'}
      >
        <BookOpen size={16} />
        <span style={{ fontWeight: '500' }}>
          {isOpen ? 'Hide Sources' : `View ${sources.length} Source${sources.length > 1 ? 's' : ''}`}
        </span>
        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>

      {isOpen && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
          {sources.map((src, idx) => (
            <div
              key={idx}
              style={{
                background: 'rgba(31, 41, 55, 0.6)',
                backdropFilter: 'blur(8px)',
                padding: '14px',
                borderRadius: '12px',
                border: '1px solid rgba(75, 85, 99, 0.5)',
                transition: 'border-color 0.3s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.4)'}
              onMouseLeave={(e) => e.currentTarget.style.borderColor = 'rgba(75, 85, 99, 0.5)'}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#60a5fa', fontWeight: '600', fontSize: '0.875rem', marginBottom: '8px' }}>
                <div style={{ padding: '4px', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '6px', display: 'flex' }}>
                  <FileText size={14} />
                </div>
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{src.source_file}</span>
                <span style={{ color: '#4b5563' }}>•</span>
                <span style={{ color: '#9ca3af', fontWeight: '400', fontSize: '0.75rem' }}>Page {src.page_number}</span>
              </div>
              <div style={{ color: '#9ca3af', fontSize: '0.875rem', lineHeight: '1.6', paddingLeft: '28px' }}>
                <span style={{ color: '#6b7280' }}>"</span>
                {src.content.substring(0, 180)}...
                <span style={{ color: '#6b7280' }}>"</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      content: 'Hello! I\'m your intelligent knowledge retrieval assistant. Upload a PDF document to get started, or ask me anything about your uploaded documents.',
      sources: [],
      timestamp: new Date().toISOString()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: input,
      sources: [],
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await axios.post('/api/chat', { question: input })

      const aiMessage = {
        role: 'ai',
        content: response.data.answer,
        sources: response.data.sources || [],
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error("Error:", error)
      setMessages(prev => [...prev, {
        role: 'ai',
        content: "I apologize, but I encountered an error connecting to the server. Please try again.",
        sources: [],
        isError: true,
        timestamp: new Date().toISOString()
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setMessages(prev => [...prev, {
      role: 'ai',
      content: `Processing ${file.name}...`,
      sources: [],
      isUploading: true,
      timestamp: new Date().toISOString()
    }])

    try {
      await axios.post('/api/ingest', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setMessages(prev => [...prev, {
        role: 'ai',
        content: `✅ Successfully processed ${file.name}! You can now ask questions about this document.`,
        sources: [],
        isSuccess: true,
        timestamp: new Date().toISOString()
      }])
    } catch (error) {
      console.error("Upload error:", error)
      setMessages(prev => [...prev, {
        role: 'ai',
        content: `❌ Failed to upload ${file.name}. Please try again.`,
        sources: [],
        isError: true,
        timestamp: new Date().toISOString()
      }])
    }

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const clearChat = () => {
    setMessages([
      {
        role: 'ai',
        content: 'Hello! I\'m your intelligent knowledge retrieval assistant. Upload a PDF document to get started, or ask me anything about your uploaded documents.',
        sources: [],
        timestamp: new Date().toISOString()
      }
    ])
  }

  return (
    <div className="app-wrapper">
      <div className="background-gradient"></div>

      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <div className="icon-wrapper">
              <div className="icon-glow"></div>
              <div className="icon-box">
                <BookOpen size={36} className="icon" />
              </div>
            </div>
            <h1 className="app-title">Intelligent Knowledge Retrieval</h1>
          </div>
          <p className="app-subtitle">Upload documents and get instant, accurate answers powered by advanced AI</p>
        </header>

        {/* Chat Container */}
        <div className="chat-wrapper">
          {/* Chat Header */}
          <div className="chat-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div className="status-indicator"></div>
              <div>
                <h2 style={{ fontSize: '0.875rem', fontWeight: '600', color: '#e5e7eb', margin: 0 }}>AI Assistant</h2>
                <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: 0 }}>Always ready to help</p>
              </div>
            </div>
            <button className="clear-btn" onClick={clearChat} title="Clear conversation">
              <Trash2 size={16} />
            </button>
          </div>

          {/* Messages Area */}
          <div className="messages-container">
            {messages.length === 1 && (
              <div className="empty-state">
                <div className="empty-state-content">
                  <MessageSquare size={48} style={{ color: '#60a5fa', marginBottom: '16px' }} />
                  <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#e5e7eb', marginBottom: '8px' }}>Start Your Conversation</h3>
                  <p style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Upload a PDF document or ask me anything to begin</p>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`message-wrapper ${msg.role === 'user' ? 'user' : 'ai'}`}>
                <div className={`message-bubble ${msg.role} ${msg.isError ? 'error' : ''} ${msg.isSuccess ? 'success' : ''}`}>
                  {msg.isError && (
                    <div className="message-status error">
                      <AlertCircle size={16} />
                      <span>Error</span>
                    </div>
                  )}
                  {msg.isSuccess && (
                    <div className="message-status success">
                      <CheckCircle2 size={16} />
                      <span>Success</span>
                    </div>
                  )}
                  {msg.isUploading && (
                    <div className="message-status uploading">
                      <Loader2 size={16} className="spinner" />
                      <span>Processing</span>
                    </div>
                  )}
                  <div className="message-content">{msg.content}</div>
                  {msg.role === 'ai' && <SourceDisplay sources={msg.sources} />}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message-wrapper ai">
                <div className="message-bubble ai">
                  <div className="loading-indicator">
                    <div className="dot-container">
                      <div className="dot" style={{ animationDelay: '0ms' }}></div>
                      <div className="dot" style={{ animationDelay: '150ms' }}></div>
                      <div className="dot" style={{ animationDelay: '300ms' }}></div>
                    </div>
                    <span>AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="input-wrapper">
            <div className="input-container">
              <button className="upload-button" onClick={() => fileInputRef.current?.click()} title="Upload PDF Document">
                <Upload size={20} />
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                  accept=".pdf"
                />
              </button>

              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSend()
                  }
                }}
                placeholder="Ask a question about your documents..."
                disabled={isLoading}
                className="message-input"
                rows={1}
              />

              <button className="send-button" onClick={handleSend} disabled={isLoading || !input.trim()}>
                <Send size={20} />
              </button>
            </div>

            <div className="input-hint">
              <Sparkles size={12} style={{ color: '#60a5fa' }} />
              <span>Press <kbd>Enter</kbd> to send • Shift + Enter for new line</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App