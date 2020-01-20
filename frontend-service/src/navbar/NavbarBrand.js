import React from 'react';
import { Link } from "react-router-dom";

export const NavbarBrand = () => (
  <div className='brand'>
    <Link to="/" className='text-decoration-none brand-name'>
      Aves<span />log
    </Link>
  </div>
);
