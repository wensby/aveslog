import React, { Suspense } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Page } from './Page.js'
import { UserProvider } from './authentication/UserContext.js';
import { WindowScrollProvider } from './WindowScrollContext.js';
import { SightingProvider } from './sighting/SightingContext.js';
import { BirdsProvider } from './bird/BirdsContext.js';
import SuspenseLoader from './suspense/SuspenseLoader';
import { AuthenticationProvider } from './authentication/AuthenticationContext.js';
import { ScrollToTop } from 'sighting/ScrollToTop.js';
import { SearchProvider } from 'search/SearchContext.js';
import { TitleProvider } from 'specific/TitleContext.js';
import { HomeProvider } from 'specific/HomeContext.js';
import { useTranslation } from 'react-i18next';

export const App = ({ version }) => {
  const { ready } = useTranslation('', { useSuspense: false });
  if (!ready) {
    return <SuspenseLoader />;
  }
  prepareLocalStorage(version);

  return (
    <TitleProvider>
      <HomeProvider>
        <BrowserRouter>
          <ScrollToTop />
          <WindowScrollProvider>
            <AuthenticationProvider>
              <UserProvider>
                <BirdsProvider>
                  <SightingProvider>
                    <SearchProvider>
                      <Suspense fallback={<SuspenseLoader />}>
                        <Page />
                      </Suspense>
                    </SearchProvider>
                  </SightingProvider>
                </BirdsProvider>
              </UserProvider>
            </AuthenticationProvider>
          </WindowScrollProvider>
        </BrowserRouter>
      </HomeProvider>
    </TitleProvider>
  );
}

/**
 * Iff the provided version differs from previously set app version in local
 * storage, clears the local storage and updates the app version.
 */
function prepareLocalStorage(version) {
  const key = 'appVersion';
  const storedVersion = localStorage.getItem(key);
  if (!storedVersion || storedVersion !== version) {
    localStorage.clear();
    localStorage.setItem(key, version);
  }
}
