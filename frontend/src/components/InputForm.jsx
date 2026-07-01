import { useState, useEffect } from 'react';
import axios from 'axios';

function InputForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    location: '',
    budget: 'Any Budget',
    cuisine: '',
    min_rating: 3.5,
    extra_preferences: ''
  });

  const [locations, setLocations] = useState([]);

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
        const response = await axios.get(`${apiBaseUrl}/api/locations`);
        if (response.data && response.data.locations) {
          setLocations(response.data.locations);
          if (response.data.locations.length > 0) {
            setFormData(prev => ({ ...prev, location: response.data.locations[0] }));
          }
        }
      } catch (err) {
        console.error("Failed to fetch locations:", err);
      }
    };
    fetchLocations();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'min_rating' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      {/* Location */}
      <div className="flex flex-col gap-2">
        <label className="font-label-md text-label-md text-secondary">Location</label>
        <div className="relative">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">location_on</span>
          <select 
            name="location"
            className="w-full pl-10 pr-4 py-3 bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none appearance-none"
            value={formData.location}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select a location</option>
            {locations.map((loc, idx) => (
              <option key={idx} value={loc}>{loc}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Cuisine */}
      <div className="flex flex-col gap-2">
        <label className="font-label-md text-label-md text-secondary">Cuisine Type</label>
        <div className="relative">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">restaurant</span>
          <select 
            name="cuisine"
            className="w-full pl-10 pr-4 py-3 bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none appearance-none" 
            value={formData.cuisine}
            onChange={handleChange}
          >
            <option value="">Any Cuisine</option>
            <option value="North Indian">North Indian</option>
            <option value="South Indian">South Indian</option>
            <option value="Chinese">Chinese</option>
            <option value="Italian">Italian</option>
            <option value="Continental">Continental</option>
            <option value="Fast Food">Fast Food</option>
            <option value="Desserts">Desserts</option>
            <option value="Beverages">Beverages</option>
            <option value="Sushi">Sushi</option>
            <option value="Vegan">Vegan</option>
          </select>
        </div>
      </div>

      {/* Budget */}
      <div className="flex flex-col gap-2">
        <label className="font-label-md text-label-md text-secondary">Budget</label>
        <select 
          name="budget"
          className="w-full px-4 py-3 bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none appearance-none"
          value={formData.budget}
          onChange={handleChange}
        >
          <option>Any Budget</option>
          <option>Low (₹)</option>
          <option>Medium (₹₹)</option>
          <option>High (₹₹₹)</option>
        </select>
      </div>

      {/* Min Rating */}
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <label className="font-label-md text-label-md text-secondary">Minimum Rating</label>
          <span className="font-label-md text-primary" id="rating-val-sidebar">{formData.min_rating}+</span>
        </div>
        <input 
          name="min_rating"
          type="range" 
          min="1" 
          max="5" 
          step="0.5" 
          className="w-full h-2 bg-secondary-container rounded-lg appearance-none cursor-pointer accent-primary" 
          value={formData.min_rating}
          onChange={handleChange}
        />
      </div>

      {/* Vibes */}
      <div className="flex flex-col gap-2">
        <label className="font-label-md text-label-md text-secondary">Extra Preferences (Vibe)</label>
        <textarea 
          name="extra_preferences"
          className="w-full px-4 py-3 bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary transition-all outline-none resize-none" 
          placeholder="e.g. romantic rooftop, quiet workspace..." 
          rows="4"
          value={formData.extra_preferences}
          onChange={handleChange}
        ></textarea>
      </div>

      {/* CTA */}
      <button 
        type="submit" 
        className="w-full bg-primary text-on-primary py-4 rounded-xl font-headline-md text-headline-md hover:bg-primary-container active:scale-95 transition-all flex items-center justify-center gap-2 group"
      >
        <span>Find Restaurants</span>
        <span className="material-symbols-outlined transition-transform group-hover:translate-x-1">auto_awesome</span>
      </button>
    </form>
  );
}

export default InputForm;
