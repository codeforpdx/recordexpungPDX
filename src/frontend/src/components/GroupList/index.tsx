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

    }

    public render() {
        return (
            <section className="cf bg-white shadow br3 mb5">
                <div className="pv4 ph3">
                    <h1 className="f3 fw6 dib">Groups</h1>
                    <button className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 fr">
                        New Group
                    </button>
                </div>

                <div className="overflow-auto">
                <table className="f6 w-100 mw8 center" data-cellspacing="0">
                    <thead>
                            <tr>
                                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">Name</th>
                                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">Role</th>
                                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">
                                Group
                            </th>
                        </tr>
                    </thead>
                </table>
                </div>
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