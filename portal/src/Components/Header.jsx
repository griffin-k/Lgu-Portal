import React from 'react';

const Header = () => {
  return (
    <header className="bg-gray-800 text-white p-4">
      <div className="container flex justify-between items-center">
        <div className="text-xl font-semibold">Your Logo</div>
        <nav>
          <ul className="flex space-x-4">
            <li className="hover:text-gray-300">Home</li>
            <li className="hover:text-gray-300">About</li>
            <li className="hover:text-gray-300">Services</li>
            <li className="hover:text-gray-300">Contact</li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
