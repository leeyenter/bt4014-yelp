import React, { Component } from 'react';
import './App.scss';
import 'semantic-ui-css/semantic.min.css';

import { Container, Menu, MenuItem } from 'semantic-ui-react';
import { NavLink, BrowserRouter as Router, Route } from 'react-router-dom';
import OverviewPage from './components/OverviewPage';
import BusinessPage from './components/BusinessPage';
import LocationPage from './components/LocationPage';

class App extends Component {
	render() {
		return (
			<div>
				<Router>
					<Container>
						<div>
							<Menu>
								<NavLink to="/" exact className="item">
									Overview
								</NavLink>
								<NavLink to="/business" className="item">
									Business
								</NavLink>
								<NavLink to="/location" className="item">
									Location
								</NavLink>
							</Menu>
							<div className="ui segment">
                <Route exact path='/' component={OverviewPage} />
                <Route path='/business' component={BusinessPage} />
                <Route path='/location' component={LocationPage} />
              </div>
						</div>
					</Container>
				</Router>
			</div>
		);
	}
}

export default App;
