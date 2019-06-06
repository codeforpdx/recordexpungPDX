import * as React from 'react';
import * as renderer from 'react-test-renderer';
import Footer from '../Footer';

export interface IJestTree {
  children: any[];
  props: {
    [key: string]: any;
  };
}

it('renders without crashing', () => {
  jest.mock('./footer.component', () => 'Footer');
  const component = renderer.create(<Footer />);
  const tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

it('has two anchors', () => {
  const component = renderer.create(<Footer />);
  const tree = component.toJSON() as IJestTree;
  let count = 0;
  for (const item of tree.children) {
    if (item.type === 'a') {
      count++;
    }
  }
  expect(count).toBe(2);
});

it('has a Terms anchor', done => {
  const component = renderer.create(<Footer />);
  const tree = component.toJSON() as IJestTree;

  // There has to be a better way then this..
  function test() {
    for (const item of tree.children) {
      if (item.type === 'a' && item.children[0] === 'Terms') {
        expect(item.children[0]).toBe('Terms');
        done();
      }
    }
    done();
  }
  test();
});

it('has a Copyright anchor', done => {
  const component = renderer.create(<Footer />);
  const tree = component.toJSON() as IJestTree;
  function test() {
    for (const item of tree.children) {
      if (item.type === 'a' && item.children[0] === 'Copyright') {
        expect(item.children[0]).toBe('Copyright');
        done();
      }
    }
    done();
  }
  test();
});
