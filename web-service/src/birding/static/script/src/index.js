'use strict';

import Navbar from './navbar.js';

const menuItems = function() {
  let items = [];
  const itemLinks = document.querySelectorAll('#sidebarList a');
  [].forEach.call(itemLinks, function(link) {
    const href = link.getAttribute('href');
    const text = link.innerText;
    items.push({
      href: href,
      text: text
    });
  });
  for (const link in itemLinks) {

  }
  return items;
};

const items = menuItems();

const navbarContainer = document.querySelector('#navbar');
ReactDOM.render(<Navbar items={items}/>, navbarContainer);