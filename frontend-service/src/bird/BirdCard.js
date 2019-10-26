import React from 'react';
import BirdCardPicture from './BirdCardPicture';
import BirdLink from './BirdLink';

export default function BirdCard({ bird, children }) {
  return (
    <div className="card">
      <div className="card-horizontal">
        <div className="img-square-wrapper">
          <BirdLink bird={bird} >
            <BirdCardPicture bird={bird} />
          </BirdLink>
        </div>
        {children}
      </div>
    </div>
  );
};
