import React, { useState, useEffect, useLayoutEffect, useContext, useRef } from 'react';
import { ScrollContext } from './ScrollContext';

export const LazyLoad = ({ offset, placeholder, children, ...props }) => {
  const [visible, setVisible] = useState(false);
  const [triggered, setTriggered] = useState(true);
  const triggeredRef = useRef(triggered);
  triggeredRef.current = triggered;
  const placeholderRef = React.createRef();
  const windowScroll = useWindowScroll(!visible);

  useEffect(() => {
    if (!triggered && !visible) {
      setTriggered(true);
    }
  }, [windowScroll, triggered, visible]);

  useLayoutEffect(() => {
    if (!visible && triggered && placeholderRef.current) {
      const pos = placeholderRef.current.getBoundingClientRect().top;
      setTimeout(() => {
        if (placeholderRef.current && triggeredRef.current) {
          const fromVisible = pos - (window.screenY + window.innerHeight);
          if (fromVisible < offset) {
            setVisible(true);
            setTriggered(false);
          }
        }
      }, 10);
    }
  }, [triggered, windowScroll, placeholderRef]);

  if (visible) {
    return <React.Fragment {...props}>{children}</React.Fragment>;
  }
  else {
    return React.cloneElement(placeholder, { ref: placeholderRef, ...props });
  }
}

const useWindowScroll = (active) => {
  const { windowScroll } = useContext(ScrollContext);
  if (active) {
    return windowScroll;
  }
  return 0;
};
