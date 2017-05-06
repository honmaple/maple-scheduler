export function lazyload(name) {
  return function(resolve) {
    require(['components/' + name], resolve);
  };
}
