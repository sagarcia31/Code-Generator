import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import AddProduto from './components/AddProduto';

function AppRoutes() {
    return (
        <Router>
            <Switch>
                <Route path="/add-produto" component={AddProduto} />
            </Switch>
        </Router>
    );
}

export default AppRoutes;