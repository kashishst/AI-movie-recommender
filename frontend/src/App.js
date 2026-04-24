import { useState } from 'react'
import './App.css'

function App() {
  const [genre, setGenre] = useState('')
  const [mood, setMood] = useState('')
  const [type, setType] = useState('')
  
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const getRecommendations = async (e) => {
    e.preventDefault()

    // show error instead of doing nothing
    if (!genre && !mood && !type) {
      setError("Please select at least one option")
      return
    }

    //clears previous errors and old results
    setLoading(true)
    setError('')
    setRecommendations([])
    
    try {
      const response = await fetch('http://127.0.0.1:5000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ genre, mood, type })
      })

      const data = await response.json()

      if (response.ok) {
        setRecommendations(data.recommendations)
      } else {
        setError(data.error)
      }
    } catch (err) {
      // error message
      setError("Cannot connect to server. Make sure Flask is running on port 5000.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🎬 AI MOVIE RECOMMENDER</h1>
      <p>Tell us what you want we will do the rest !!!!!</p>

      <form onSubmit={getRecommendations} className="form-box">

        <select value={genre} onChange={(e) => setGenre(e.target.value)}>
          <option value="">Select Genre</option>
          <option value="Action">Action</option>
          <option value="Comedy">Comedy</option>
          <option value="Drama">Drama</option>
          <option value="Horror">Horror</option>
          <option value="Romance">Romance</option>
          <option value="Thriller">Thriller</option>
        </select>

        <select value={mood} onChange={(e) => setMood(e.target.value)}>
          <option value="">Select Mood</option>
          <option value="happy">Happy</option>
          <option value="sad">Sad</option>
          <option value="excited">Excited</option>
          <option value="romantic">Romantic</option>
          <option value="scared">Scared</option>
        </select>

        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="">Select Type</option>
          <option value="funny">Funny</option>
          <option value="dark">Dark</option>
          <option value="emotional">Emotional</option>
          <option value="intense">Intense</option>
        </select>

        {/* ✅ FIX 4: disable button while loading */}
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Get Recommendations"}
        </button>

      </form>

      {error && <p className="error">{error}</p>}

      {recommendations.length > 0 && (
        <div className="results">
          <h2>🎯 Recommended Movies</h2>
          
          <div className="movie-list">
            {recommendations.map((movie, index) => (
              <div key={index} className="movie-card">
                <h3>{movie.title}</h3>
                <p>⭐ IMDB: {movie.rating}</p>
                <p>🎭 {movie.genre}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App