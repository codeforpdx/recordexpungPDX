import React from 'react';
import { Group as GroupTypes } from '../../redux/groups/types';

interface Props {
  group: GroupTypes;
}

class Group extends React.Component<Props> {
  public render() {
    return (         
      <div className="bt br bl b--black-10 flex-ns justify-between flex-wrap items-center">
        <div className="pa3">{this.props.group.name}</div>
        <div className="pa3">
          <span className="pr3">
          {this.props.group.users.length}
            <span className="visually-hidden">User count</span>
            <i aria-hidden="true" className="fa fa-user pl1"></i>
          </span>
          <button aria-label="edit group" className="navy hover-dark-blue">
            <i aria-hidden="true" className="fa fa-pen pr3"></i>
          </button>
          <button aria-label="delete group" className="navy hover-dark-blue">
            <i aria-hidden="true" className="fa fa-trash"></i>
          </button>
        </div>
      </div>
    );
  }
}

export default Group;
