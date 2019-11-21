import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { loadGroups } from '../../redux/groups/actions';
import { Group as GroupTypes, GroupState } from '../../redux/groups/types';
import Group from '../Group';

interface Props {
  groups: GroupState;
  loadGroups: Function;
}

class GroupList extends React.Component<Props> {
    public componentWillMount() {
      // this will call the axios request to populate the component with groupList
      this.props.loadGroups();
    }

    public displayGroups = (inputGroups: GroupTypes[]) => {
      if (inputGroups) {
        const returnList = inputGroups.map(group => {
          return <Group key={group.id} group={group} />;
        });

        return returnList
      }
    }

    public render() {
        return (
          <section className="cf bg-white shadow br3 mt5 mb3">
            <div className="pv4 ph3">
              <h1 className="f3 fw6 dib">Groups</h1>
              <button 
                aria-expanded="true"
                aria-controls="new_group"
                className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 fr">
                New Group
              </button>
              <form id="new_group" className="pt4">
                <legend className="visually-hidden">Create new group</legend>
                <label htmlFor="new-group-name" className="db mb1 fw6">New Group Name</label>
                <div className="flex items-center">
                  <input id="new-group-name" className="pa2 br2 b--black-20"/>
                  <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 ml2">Save</button>
                  <button className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 ml2">Cancel</button>
                </div>
              </form>
            </div>
            {this.props.groups 
              ? this.displayGroups(this.props.groups.groupList)
              : null}
          </section>
        );
    }
}

const mapStatetoProps = (state: AppState) => ({
  groups: state.groups
});

export default connect(
  mapStatetoProps,
  { loadGroups }
)(GroupList)