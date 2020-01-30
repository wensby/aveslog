import React from 'react';
import { Label } from './Label';
import { useBirdName } from '../bird/BirdHooks';

export function BirdSection({ bird }) {
  const { local, binomial, loading } = useBirdName(bird);

  return (
    <div className='form-group row'>
      <Label htmlFor='birdInput' label='bird-label' />
      <div className='col-sm-10'>
        <input id='birdInput' type='text' readOnly className='col-sm-10 form-control-plaintext' value={loading ? '' : local || binomial} />
      </div>
    </div>
  );
}
