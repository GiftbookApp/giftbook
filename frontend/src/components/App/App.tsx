import { ROUTES } from 'components/App/routes';
import Home from 'components/Home/Home';
import React from 'react';
import { Route, Routes } from 'react-router';
import './App.scss';

const App: React.FC = () => {
  return <Routes>
    <Route path={ROUTES.HOME} element={<Home />} />
  </Routes>;
};

export default App;