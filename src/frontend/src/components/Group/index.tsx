import React from 'react';
import { Group as GroupTypes } from '../../redux/groups/types';

interface Props {
  group: GroupTypes;
}

class Group extends React.Component<Props> {
  public render() {
    return (
      <tr>
        <td className="pa3 bb b--black-20">
          <a href="#" className="underline">
            {this.props.group.name}
          </a>
        </td>
        <td className="pa3 bb b--black-20">{this.props.group.name}</td>
        <td className="pa3 bb b--black-20">{this.props.group.users.length}</td>
      </tr>
    );
  }
}

export default Group;
