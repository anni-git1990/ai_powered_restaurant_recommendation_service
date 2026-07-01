import { useState } from 'react'
import axios from 'axios'
import InputForm from './components/InputForm'
import ResultsDisplay from './components/ResultsDisplay'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (formData) => {
    setLoading(true)
    setError(null)
    setResults(null)

    // Smooth scroll to results on mobile, or just top of results grid
    const resultsArea = document.getElementById('results-area')
    if (resultsArea) {
      resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }

    try {
      // Clean up empty fields
      const payload = { ...formData }
      if (!payload.budget || payload.budget === 'Any Budget') delete payload.budget
      if (!payload.cuisine) delete payload.cuisine
      if (!payload.extra_preferences) delete payload.extra_preferences

      // We need to map standard budgets to exactly what the backend expects
      if (payload.budget) {
        if (payload.budget.includes('Low')) payload.budget = 'low';
        else if (payload.budget.includes('Medium')) payload.budget = 'medium';
        else if (payload.budget.includes('High')) payload.budget = 'high';
      }

      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
      const response = await axios.post(`${apiBaseUrl}/api/recommend`, payload)
      setResults(response.data.candidates)
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail)
      } else {
        setError("Failed to connect to the recommendation engine. Please ensure the backend is running.")
      }
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <header className="fixed top-0 w-full z-50 bg-surface/80 dark:bg-surface-dim/80 backdrop-blur-md shadow-sm flex justify-between items-center px-4 md:px-10 h-16">
        <div className="font-headline-lg text-headline-lg font-bold text-primary">CulinaAI</div>
        <div className="hidden md:flex gap-8 items-center">
          <a className="text-primary font-bold transition-colors" href="#">Explore</a>
          <a className="text-secondary font-medium hover:text-primary-container transition-colors" href="#">History</a>
          <a className="text-secondary font-medium hover:text-primary-container transition-colors" href="#">AI Concierge</a>
          <div className="flex items-center gap-4 border-l pl-8 border-outline-variant">
            <span className="material-symbols-outlined text-secondary cursor-pointer hover:text-primary transition-colors">notifications</span>
            <span className="material-symbols-outlined text-secondary cursor-pointer hover:text-primary transition-colors">favorite</span>
            <div className="w-8 h-8 rounded-full overflow-hidden border border-primary/20">
              <img className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCph0k-T3JcnlIqsDytCNGmwBe6dBeKbxwlNbxPAoH-FTzaB_ETUeUaG2OKQu0EvuV0_jvSvy0TFMBPMYjuxL6omiwHR4mSD5NWepi9j26FCop2O4kyANaBOda1QN3KdjxJbIWCktKKyBlEtQQ2qtUhM-Qe-JHnl3dGjQ5tXraeJMjYoQWjMSZO3HC-31LXYo2nORQ1f5Juj7XLAIvpdGn085z9mvygJNid4BGIw6XjgS0e0IZXf-VC2TeS3U2sAYVAQq9AePd8ZXA" alt="Profile" />
            </div>
          </div>
        </div>
        <div className="md:hidden flex items-center gap-4">
          <span className="material-symbols-outlined text-primary">menu</span>
        </div>
      </header>

      <div className="flex pt-16 min-h-screen">
        {/* Sidebar Control Panel */}
        <aside className="hidden md:block w-[350px] fixed left-0 top-16 bottom-0 bg-surface-container-low border-r border-outline-variant overflow-y-auto sidebar-scroll z-40">
          <div className="p-lg space-y-8">
            <div className="space-y-1">
              <h2 className="font-headline-md text-headline-md text-on-background">Filter Results</h2>
              <p className="text-secondary font-body-md">Refine your AI recommendations</p>
            </div>
            <InputForm onSubmit={handleSearch} />
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 md:ml-[350px] p-4 md:p-lg lg:p-xl transition-all">
          <section className="max-w-7xl mx-auto" id="results-area">
            {error && (
              <div className="p-4 mb-8 bg-error-container text-on-error-container rounded-xl border border-error">
                {error}
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center py-20 gap-8" id="loading-state">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full border-4 border-primary/20 flex items-center justify-center pulsate">
                    <span className="material-symbols-outlined text-primary text-5xl">auto_awesome</span>
                  </div>
                  <div className="absolute inset-0 w-24 h-24 rounded-full border-t-4 border-primary animate-spin"></div>
                </div>
                <div className="text-center">
                  <h3 className="font-headline-md text-headline-md text-on-background mb-2">Analyzing your preferences...</h3>
                  <p className="font-body-md text-body-md text-secondary">Our AI is curating the perfect recommendations for you.</p>
                </div>
              </div>
            )}

            {!loading && results && (
              <ResultsDisplay results={results} />
            )}
            
            {/* Show an empty state if no search yet */}
            {!loading && !results && !error && (
               <div className="flex flex-col items-center justify-center py-20 gap-4 opacity-60">
                 <span className="material-symbols-outlined text-6xl text-secondary">manage_search</span>
                 <p className="font-body-lg text-secondary text-center max-w-md">Use the filters on the left to discover the perfect dining spot tailored to your taste.</p>
               </div>
            )}
          </section>
        </main>
      </div>

      <nav className="md:hidden fixed bottom-0 left-0 w-full flex justify-around items-center h-20 px-4 pb-safe bg-surface/95 dark:bg-surface-container/95 backdrop-blur-sm shadow-[0px_-4px_20px_rgba(0,0,0,0.05)] z-50 rounded-t-xl">
        <a className="flex flex-col items-center justify-center text-primary bg-primary-container/10 rounded-xl p-2 active:scale-90 transition-all duration-200" href="#">
          <span className="material-symbols-outlined">explore</span>
          <span className="font-label-md text-label-md">Explore</span>
        </a>
        <a className="flex flex-col items-center justify-center text-secondary p-2 active:scale-90 transition-all duration-200" href="#">
          <span className="material-symbols-outlined">history</span>
          <span className="font-label-md text-label-md">History</span>
        </a>
        <a className="flex flex-col items-center justify-center text-secondary p-2 active:scale-90 transition-all duration-200" href="#">
          <span className="material-symbols-outlined">auto_awesome</span>
          <span className="font-label-md text-label-md">AI</span>
        </a>
        <a className="flex flex-col items-center justify-center text-secondary p-2 active:scale-90 transition-all duration-200" href="#">
          <span className="material-symbols-outlined">person</span>
          <span className="font-label-md text-label-md">Profile</span>
        </a>
      </nav>
    </>
  )
}

export default App
