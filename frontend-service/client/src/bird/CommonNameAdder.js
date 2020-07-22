import React, { useState, useRef, useEffect } from 'react';
import Icon from '../Icon.js';
import './CommonNameAdder.scss';
import { CommonNameForm } from './CommonNameForm';

export function CommonNameAdder({ bird, locales, onNameAdded }) {
  const [expanded, setExpanded] = useState(false);
  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef, () => { setExpanded(false) });
  const activate = e => {
    e.preventDefault();
    setExpanded(true);
  };

  const handleNamedAdded = (language, name) => {
    setExpanded(false);
    onNameAdded(language, name);
  }

  if (expanded) {
    return (
      <div ref={wrapperRef} className={'common-name-adder' + (expanded ? ' expanded' : '')}>
        <CommonNameForm bird={bird} locales={locales} onNameAdded={handleNamedAdded} />
      </div>
    );
  }
  else {
    return (
      <div className='common-name-adder' onClick={activate} >
        <Icon name='add' />
      </div>
    );
  }
}

function useOutsideAlerter(ref, onClickOutside) {
  function handleClickOutside(event) {
    if (ref.current && !ref.current.contains(event.target)) {
      onClickOutside();
    }
  }

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  });
}
