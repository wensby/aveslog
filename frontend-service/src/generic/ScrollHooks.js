import { useState, useEffect, useContext, useRef, useLayoutEffect } from 'react';
import { WindowScrollContext } from '../WindowScrollContext';

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
