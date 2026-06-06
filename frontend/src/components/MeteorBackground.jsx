import React, { useEffect, useState } from "react";
import "./MeteorBackground.css";

function MeteorBackground() {
  const [stars, setStars] = useState([]);
  const [meteors, setMeteors] = useState([]);

  useEffect(() => {
    // Generate twinkling stars
    const newStars = Array.from({ length: 60 }).map((_, i) => ({
      id: i,
      top: Math.random() * 100,
      left: Math.random() * 100,
      size: 1 + Math.random() * 2,
      delay: Math.random() * 5,
      duration: 2 + Math.random() * 3,
    }));
    setStars(newStars);

    // Generate static values for meteors to avoid constant regenerations
    const newMeteors = Array.from({ length: 8 }).map((_, i) => ({
      id: i,
      top: Math.random() * 50, // start from upper portion
      left: 30 + Math.random() * 60, // scatter across width
      delay: Math.random() * 12,
      duration: 6 + Math.random() * 6,
    }));
    setMeteors(newMeteors);
  }, []);

  return (
    <div className="meteor-background">
      {/* Twinkling stars */}
      <div className="stars-container">
        {stars.map((star) => (
          <div
            key={star.id}
            className="twinkle-star"
            style={{
              top: `${star.top}%`,
              left: `${star.left}%`,
              width: `${star.size}px`,
              height: `${star.size}px`,
              animationDelay: `${star.delay}s`,
              animationDuration: `${star.duration}s`,
            }}
          />
        ))}
      </div>
      {/* Meteor trails */}
      <div className="meteors-container">
        {meteors.map((meteor) => (
          <div
            key={meteor.id}
            className="meteor"
            style={{
              top: `${meteor.top}%`,
              left: `${meteor.left}%`,
              animationDelay: `${meteor.delay}s`,
              animationDuration: `${meteor.duration}s`,
            }}
          />
        ))}
      </div>
    </div>
  );
}

export default MeteorBackground;
