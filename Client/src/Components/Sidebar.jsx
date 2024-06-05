import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaChartLine, FaTable, FaBars } from 'react-icons/fa';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const closeSidebar = () => {
    setIsOpen(false);
  };

  return (
    <>
      {/* Hamburger Icon for mobile view */}
      <div className="md:hidden p-4 bg-blue-700 text-white">
        <FaBars className="text-2xl cursor-pointer" onClick={toggleSidebar} />
      </div>

      <div className={`bg-blue-700 text-white min-h-screen p-4 fixed top-0 left-0 md:relative w-64 ${isOpen ? 'block' : 'hidden'} md:block`}>
        <div className="mb-8">
          <h1 className="text-2xl font-bold">Student Graduation Rate</h1>
        </div>
        <nav>
          <ul>
            <li className="mb-4">
              <NavLink to="/" className={({ isActive }) => (isActive ? "text-blue-300" : "")} onClick={closeSidebar}>
                <FaHome className="inline-block mr-2" /> Home
              </NavLink>
            </li>
            <li className="mb-4">
              <NavLink to="/predict-many" className={({ isActive }) => (isActive ? "text-blue-300" : "")} onClick={closeSidebar}>
                <FaChartLine className="inline-block mr-2" /> Predict Many
              </NavLink>
            </li>
            <li className="mb-4">
              <NavLink to="/predict-single" className={({ isActive }) => (isActive ? "text-blue-300" : "")} onClick={closeSidebar}>
                <FaChartLine className="inline-block mr-2" /> Predict Single
              </NavLink>
            </li>
            <li className="mb-4">
              <NavLink to="/results" className={({ isActive }) => (isActive ? "text-blue-300" : "")} onClick={closeSidebar}>
                <FaTable className="inline-block mr-2" /> Table
              </NavLink>
            </li>
            <li className="mb-4">
              <NavLink to="/users" className={({ isActive }) => (isActive ? "text-blue-300" : "")} onClick={closeSidebar}>
                <FaTable className="inline-block mr-2" /> User Management
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default Sidebar;
