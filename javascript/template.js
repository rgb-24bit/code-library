/**
 * Produces a function which uses template strings to do simple interpolation from objects.
 *
 * Usage:
 *     var makeMeKing = generateTemplateString('${name} is now the king of ${country}!');
 *
 *     console.log(makeMeKing({ name: 'Bryan', country: 'Scotland'}));
 *     // Logs 'Bryan is now the king of Scotland!'
 *
 * Refrence:
 *     https://gist.github.com/bryanerayner/68e1498d4b1b09a30ef6
 */
const generateTemplateString = (function() {
  let cache = {};

  function generateTemplate(template) {
    let fn = cache[template];

    if (fn === undefined) {
      // Replace ${expressions} (etc) with ${map.expressions}.

      let sanitized = template
          .replace(/\$\{([\s]*[^;\s\{]+[\s]*)\}/g, function(_, match) {
            return `\$\{map.${match.trim()}\}`;
          })

      // Afterwards, replace anything that's not ${map.expressions}' (etc) with a blank string.
          .replace(/(\$\{(?!map\.)[^}]+\})/g, '');

      fn = Function('map', `return \`${sanitized}\``);
    }
    return fn;
  };
  return generateTemplate;
})();
