import React, { useState, useEffect, useContext, useRef, useLayoutEffect, forwardRef } from 'react';
import { WindowScrollContext } from '../WindowScrollContext';

/**
 * Returns true when the component associated with the argument ref is within
 * the offset of being revealed, vertically.
 */
export const useReveal = (componentRef, offset) => {
  const [revealed, setRevealed] = useState(false);
  const [triggered, setTriggered] = useState(true);
  const windowScroll = useWindowScroll(!revealed);
  const triggeredRef = useRef(triggered);
  triggeredRef.current = triggered;

  useEffect(() => {
    if (!triggered && !revealed) {
      setTriggered(true);
    }
  }, [windowScroll, triggered, revealed]);

  useLayoutEffect(() => {
    if (!revealed && triggered && componentRef.current) {
      const pos = componentRef.current.getBoundingClientRect().top;
      setTimeout(() => {
        if (componentRef.current && triggeredRef.current) {
          const fromVisible = pos - (window.screenY + window.innerHeight);
          if (fromVisible < offset) {
            setRevealed(true);
            setTriggered(false);
          }
        }
      }, 10);
    }
  }, [triggered, windowScroll, componentRef]);

  return revealed;
}

export const useWindowScroll = active => {
  const { windowScroll } = useContext(WindowScrollContext);
  if (active) {
    return windowScroll;
  }
  return 0;
};

const withRevealingRef = WrappedComponent => {
  return props => {
    const ref = useRef(null);
    const revealed = useReveal(ref, 1000);
    return <WrappedComponent ref={ref} revealed={revealed} {...props} />
  };
};

/**
 * Higher order component for giving the wrapped component a reveal prop,
 * informing it when it has been scrolled into view and revealed.
 */
export const withReveal = WrappedComponent => (
  withRevealingRef(forwardRef(WrappedComponent))
);
