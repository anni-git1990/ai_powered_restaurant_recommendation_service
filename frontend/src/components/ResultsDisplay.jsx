function ResultsDisplay({ results }) {
  if (!results || results.length === 0) {
    return null;
  }

  return (
    <>
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="font-headline-lg text-headline-lg text-on-background">AI Curated Picks</h2>
          <p className="text-secondary">Hand-picked experiences matching your vibe.</p>
        </div>
        <button className="flex items-center gap-2 text-primary font-label-md">
          Sort by: AI Match <span className="material-symbols-outlined">expand_more</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-gutter">
        {results.map((restaurant, index) => (
          <div key={index} className="group bg-surface-container-lowest rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-outline-variant/30 flex flex-col">
            <div className="p-md space-y-4 flex-grow flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-1">
                  <h3 className="font-headline-md text-headline-md text-on-background pr-2">{restaurant.name}</h3>
                  <div className="bg-surface-container-low px-2 py-1 rounded-lg flex items-center gap-1 shrink-0 border border-outline-variant/50">
                    <span className="material-symbols-outlined text-[16px] text-[#FFBA00]" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                    <span className="font-bold text-on-surface text-sm">{restaurant.rating}</span>
                  </div>
                </div>
                <div className="mb-3 flex justify-between items-center text-secondary font-label-md text-sm">
                  <span>₹{restaurant.cost} for two • {restaurant.location}</span>
                  {restaurant.zomato_url && restaurant.zomato_url !== 'nan' && restaurant.zomato_url !== 'None' && (
                    <a href={restaurant.zomato_url.startsWith('http') ? restaurant.zomato_url : `https://${restaurant.zomato_url}`} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline flex items-center gap-1">
                      Link <span className="material-symbols-outlined text-[14px]">open_in_new</span>
                    </a>
                  )}
                </div>
                <div className="flex gap-2 flex-wrap mb-4">
                  {restaurant.cuisines && restaurant.cuisines.split(',').map((c, i) => (
                    <span key={i} className="text-label-sm font-label-sm text-secondary px-2 py-0.5 bg-surface-container rounded border border-outline-variant">
                      {c.trim()}
                    </span>
                  ))}
                </div>
              </div>
              
              {/* AI Explanation Box */}
              {restaurant.explanation && (
                <div className="p-4 bg-primary/5 border-l-4 border-primary rounded-r-xl mt-auto">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="material-symbols-outlined text-primary text-[16px]">auto_awesome</span>
                    <span className="text-[10px] font-bold text-primary uppercase tracking-wider">AI Insight</span>
                  </div>
                  <p className="text-sm text-on-surface-variant leading-relaxed">
                    {restaurant.explanation}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default ResultsDisplay;
