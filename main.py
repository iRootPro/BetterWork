import sj
import hh
from table import get_table

def main():
    get_table(sj.get_languages(), 'SuperJob')
    get_table(hh.get_languages(), 'HeadHunter')

if __name__ == '__main__':
    main()
