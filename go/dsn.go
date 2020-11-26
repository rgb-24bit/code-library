// Package dsn implementation a simple dsn parser
//
// Example:
//
// func main() {
//     var uri = MakeDsn("uri", "[scheme://]host[:port]path[?query][#fragment]", map[string]string{
//         "scheme":   `\w+`,
//         "host":     `[\w.]+`,
//         "port":     `\d+`,
//         "path":     `[\w/.]+`,
//         "query":    `[^#]+`,
//         "fragment": `.+`,
//     })
//
//     var res = uri.Parse("https://www.google.com/search?q=dsn&oq=dsn&aqs=chrome.0.69i59l4j0i131i433j69i61j69i60l2.935j0j7&sourceid=chrome&ie=UTF-8")
//     fmt.Println(res)
// }
//
// output:
//   map[host:www.google.com path:/search query:q=dsn&oq=dsn&aqs=chrome.0.69i59l4j0i131i433j69i61j69i60l2.935j0j7&sourceid=chrome&ie=UTF-8 scheme:https]
package dsn

import (
	"regexp"
	"strings"
)

/** dsn **/

type Dsn struct {
	Name   string
	Define string
	parser *Parser
	tokens []*Token
}

func MakeDsn(name, define string, patterns map[string]string) *Dsn {
	dsn := &Dsn{Name: name, Define: define}

	dsn.tokens = ScanTokens(define)
	dsn.parser = MakeParser(dsn.tokens, patterns)

	return dsn
}

func (d *Dsn) Parse(text string) map[string]string {
	result, _ := d.parser.Parse(text)
	return result
}

/** parser **/

const (
	TypeName = "Name"
	TypeSep  = "Sep"
	TypeOpt  = "Opt"
)

type Parser struct {
	Type       string
	Name       string
	Pattern    *regexp.Regexp
	OptParsers []*Parser
}

func MakeParser(tokens []*Token, _patterns map[string]string) *Parser {
	var patterns = make(map[string]*regexp.Regexp)
	var parsers = []*Parser{{}}
	var last = 0

	for k, v := range _patterns {
		patterns[k] = regexp.MustCompile("^" + v)
	}

	for _, token := range tokens {
		switch token.Type {
		case "NAME":
			parsers[last].OptParsers = append(parsers[last].OptParsers, &Parser{Name: token.Value, Type: TypeName, Pattern: patterns[token.Value]})
		case "SEP":
			pattern := regexp.QuoteMeta(token.Value)
			parsers[last].OptParsers = append(parsers[last].OptParsers, &Parser{Name: token.Value, Type: TypeSep, Pattern: regexp.MustCompile("^" + pattern)})
		case "LP":
			parsers = append(parsers, &Parser{Type: TypeOpt})
			last++
		case "RP":
			parsers[last-1].OptParsers = append(parsers[last-1].OptParsers, parsers[last])
			parsers = parsers[:last]
			last--
		}
	}

	return parsers[last]
}

func (p *Parser) Parse(text string) (map[string]string, string) {
	var result = make(map[string]string)

	var base = text

	for _, optParser := range p.OptParsers {
		switch optParser.Type {
		case TypeName, TypeSep:
			matched := optParser.Pattern.FindString(text)

			if matched == "" {
				return nil, base
			}

			if optParser.Type == TypeName {
				result[optParser.Name] = matched
			}

			text = text[len(matched):]
		case TypeOpt:
			optResult, next := optParser.Parse(text)
			for k, v := range optResult {
				result[k] = v
			}
			text = next
		}
	}

	return result, text
}

func (p *Parser) String() string {
	return fmt.Sprintf("Parser(%v, %v, %v, %v)", p.Type, p.Name, p.Pattern, p.OptParsers)
}

/** scanner **/

var tokens = []string{
	`(?P<NAME>\w+)`,
	`(?P<LP>\[)`,
	`(?P<RP>\])`,
	`(?P<SEP>[^\w\[\]]+)`,
}

type Token struct {
	Type  string
	Value string
}

func (t *Token) String() string {
	return fmt.Sprintf("Token(%s, %s)", t.Type, t.Value)
}

func ScanTokens(text string) []*Token {
	reg := regexp.MustCompile(strings.Join(tokens, "|"))

	res := make([]*Token, 0)
	grp := reg.SubexpNames()

	for _, matched := range reg.FindAllStringSubmatch(text, -1) {
		for i, match := range matched {
			if i > 0 && match != "" {
				res = append(res, &Token{Value: match, Type: grp[i]})
			}
		}
	}

	return res
}

