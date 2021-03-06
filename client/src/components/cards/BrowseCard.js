/* Copyright 2018 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import React, { Component } from 'react';
import StackedAvatar from '../avatar/StackedAvatar';
import { Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './BrowseCard.css';


/**
 *
 * @class         BrowseCard
 * @description   BrowseCard component
 *
 *
 */
export default class BrowseCard extends Component {

  static propTypes = {
    details: PropTypes.object,
  };


  state = { isPinned: false };


  togglePinned = () => {
    this.setState({
      isPinned: !this.state.isPinned
    });
  }


  render () {
    const { details } = this.props;
    const { isPinned } = this.state;

    return (
      <div className='browse-tile'>
        <div className='browse-tile-title'>
          <div>
            <div>{details.name}</div>
            {/* <div className='browse-tile-category'>{details.category}</div> */}
          </div>
          <div className='browse-tile-pinned-icon'>
            <Icon
              disabled={!isPinned}
              onClick={this.togglePinned}
              inverted name='pin' size='small'/>
          </div>
        </div>
        <div className='browse-tile-members'>
          <StackedAvatar list={details.owners || []}/>
        </div>
      </div>
    );
  }

}
