import React, { useState, useEffect, useContext, useRef, useLayoutEffect, forwardRef } from 'react';
import { WindowScrollContext } from '../WindowScrollContext';

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
      if (!revealed && triggered && ref.current) {
        const pos = ref.current.getBoundingClientRect().top;
        setTimeout(() => {
          if (ref.current && triggeredRef.current) {
            const fromVisible = pos - (window.screenY + window.innerHeight);
            if (fromVisible < 1000) {
              setRevealed(true);
              setTriggered(false);
            }
          }
        }, 10);
      }
    }, [triggered, windowScroll, ref]);

    return <WrappedComponent ref={ref} revealed={revealed} {...props} />
  };
};

/**
 * Higher order component for giving the wrapped component a reveal prop and
 * ref that's attached to the DOM element that will be "revealed". Thus, the
 * wrapped component will get informed when it's DOM element has been scrolled
 * into view and revealed.
 *
 * This makes it easy to create components that should get revealed as you
 * scroll them into view, when it is important to not do expensive calculations
 * or fetches as long as they are not visible.
 */
export const withReveal = WrappedComponent => (
  withRevealingRef(forwardRef(WrappedComponent))
);
