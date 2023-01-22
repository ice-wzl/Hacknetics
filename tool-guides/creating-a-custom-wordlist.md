# Creating a Custom Wordlist

### Hashcat Rules

* Start by creating a wordlist with potential passwords&#x20;

```
January
Password
password
P@ssw0rd
Febuary
March
April
May
June
July
August
September
October
November
December
Summer
Spring
Winter
Fall
```

* Users love to have dates in their passwords along with `!`

```
for i in $(cat pwlist.txt); do echo $i; echo ${i}2019; echo $i{2020}; echo ${i}\!; done > pwlist2.txt
```

* This will keep your original entries, but also create entries with the dates and `!`:

```
December
December2019
December2020
December2019!
December2020!
December!
```

* Now use hashcat rules to create some randomness in your password list

```
hashcat --force --stdout pwlist2.txt -r /usr/share/hashcat/rules/best64.rule
```

* Now your password list should look something like this

```
--snip--
merSum
mmer!
mmer
ummer
SummSumm
fumm!
9102remmuS
Summer20190
SUMMER2019
--snip--
```

* Note for a more compressive wordlist you can also chain rules with hashcat&#x20;

```
hashcat --force --stdout pwlist2.txt -r /usr/share/hashcat/rules/best64.rule -r /usr/share/hashcat/rules/toggles1.rule
```

* `toggles1.rule` will toggle upper and lower characters, however when you do this many duplicates will exist plus long passwords
* If you only wanted passwords with 8 characters or more instead of the above command you could use `awk` in addition&#x20;

```
hashcat --force --stdout pwlist2.txt -r /usr/share/hashcat/rules/best64.rule -r /usr/share/hashcat/rules/toggles1.rule | sort -u | awk 'length($0) > 8'
```

* This command will sort by unique occurrences and also only have passwords with 8 or more chars.

### exrex Password Generator&#x20;

* [https://github.com/asciimoo/exrex](https://github.com/asciimoo/exrex)

#### Install

```
git clone https://github.com/asciimoo/exrex.git
cd exrex
easy_install exrex
--or--
pip3 install exrex
```

```
exrex "((W|w)inter|(S|s)ummer|(F|f)all|(A|a)utumn|(S|s)pring)20(16|17|18|19|20|21|22)" > seasons_months.txt
exrex "((J|j)anuary|(F|f)ebruary|(M|m)arch|(A|a)pril|(M|m)ay|(J|j)une|(J|j)uly|(A|a)ugust|(S|s)eptember|(O|o)ctober|(N|n)ovember|(D|d)ecember)20(16|17|18|19|20|21|22)" >> seasons_months.txt
```

* Will leave you with roughly 300 passwords&#x20;

### kwp Keyboard Walk Password List Generator

* Release page: [https://github.com/hashcat/kwprocessor/releases/tag/v1.00](https://github.com/hashcat/kwprocessor/releases/tag/v1.00)

<pre><code><strong>kwp -z basechars/full.base keymaps/en-us.keymap routes/2-to-16-max-3-direction-changes.route > keymap.txt
</strong><strong>#below command might explode your vm
</strong>kwp -s1 basechars/full.base keymaps/en-us.keymap routes/2-to-32-max-5-direction-changes.route -o /opt/kwprocessor/lists/lists-keepass
</code></pre>
