# https://www.timeanddate.com/date/dateadd.html to calculate dates
import pytest

from app.model.date import Date, TimePeriod


class TestTimePeriod:
    #####################
    # repr
    #####################

    def test_repr_year(self):
        assert repr(TimePeriod(years=1)) == '1 year, 0 months, 0 days'
        assert repr(TimePeriod(years=2)) == '2 years, 0 months, 0 days'

    def test_repr_month(self):
        assert repr(TimePeriod(months=1)) == '0 years, 1 month, 0 days'
        assert repr(TimePeriod(months=2)) == '0 years, 2 months, 0 days'

    def test_repr_days(self):
        assert repr(TimePeriod(days=1)) == '0 years, 0 months, 1 day'
        assert repr(TimePeriod(days=2)) == '0 years, 0 months, 2 days'

    #####################
    # eq
    #####################

    def test_eq_years_only(self):
        assert TimePeriod(years=1) == TimePeriod(years=1)

    def test_eq_months_only(self):
        assert TimePeriod(months=1) == TimePeriod(months=1)

    def test_eq_days_only(self):
        assert TimePeriod(days=1) == TimePeriod(days=1)

    #####################
    # neg
    #####################

    def test_neg(self):
        assert -TimePeriod(days=1, months=1, years=1) == TimePeriod(days=-1, months=-1, years=-1)

    #####################
    # Time wrap
    #####################

    def test_no_wrap_days(self):
        tp = TimePeriod(days=150)
        assert tp.years == 0, 'years'
        assert tp.months == 0, 'months'
        assert tp.days == 150, 'days'

    def test_month_wrap(self):
        tp = TimePeriod(months=13)
        assert tp.years == 1, 'years'
        assert tp.months == 1, 'months'

    def test_month_wrap_days(self):
        tp = TimePeriod(days=1, months=13)
        assert tp.years == 1, 'years'
        assert tp.months == 1, 'months'
        assert tp.days == 1, 'days'

    def test_month_wrap_whole_year(self):
        tp = TimePeriod(months=12)
        assert tp.years == 1, 'years'
        assert tp.months == 0, 'months'

    def test_neg_month(self):
        tp = TimePeriod(months=-1)
        assert tp.years == 0, 'years'
        assert tp.months == -1, 'months'

    def test_neg_month_wrap_whole_year(self):
        tp = TimePeriod(months=-12)
        assert tp.years == -1, 'years'
        assert tp.months == 0, 'months'

    def test_neg_month_wrap(self):
        tp = TimePeriod(months=-13)
        assert tp.years == -1, 'years'
        assert tp.months == -1, 'months'

    def test_neg_month_wrap_pos_year(self):
        tp = TimePeriod(months=-1, years=1)
        assert tp.years == 0, 'years'
        assert tp.months == 11, 'months'

    def test_neg_month_wrap_pos_year2(self):
        tp = TimePeriod(months=1, years=-1)
        assert tp.years == 0, 'years'
        assert tp.months == -11, 'months'

    def test_neg_month_wrap_pos_year3(self):
        tp = TimePeriod(months=-13, years=1)
        assert tp.years == 0, 'years'
        assert tp.months == -1, 'months'

    def test_neg_month_wrap_days(self):
        tp = TimePeriod(days=1, months=-13)
        assert tp.years == -1, 'years'
        assert tp.months == -1, 'months'
        assert tp.days == 1, 'days'


class TestDate:
    def test_empty_date(self):
        with pytest.raises(ValueError):
            Date()

    #####################
    # Days in months
    #####################

    def test_days_jan(self):
        assert Date.get_days_in_month(Date.JANUARY, 1901) == 31

    def test_days_feb(self):
        assert Date.get_days_in_month(Date.FEBRUARY, 1901) == 28

    def test_days_feb_leap_year(self):
        assert Date.get_days_in_month(Date.FEBRUARY, 2008) == 29

    def test_days_mar(self):
        assert Date.get_days_in_month(Date.MARCH, 1901) == 31

    def test_days_apr(self):
        assert Date.get_days_in_month(Date.APRIL, 1901) == 30

    def test_days_may(self):
        assert Date.get_days_in_month(Date.MAY, 1901) == 31

    def test_days_jun(self):
        assert Date.get_days_in_month(Date.JUNE, 1901) == 30

    def test_days_jul(self):
        assert Date.get_days_in_month(Date.JULY, 1901) == 31

    def test_days_aug(self):
        assert Date.get_days_in_month(Date.AUGUST, 1901) == 31

    def test_days_sep(self):
        assert Date.get_days_in_month(Date.SEPTEMBER, 1901) == 30

    def test_days_oct(self):
        assert Date.get_days_in_month(Date.OCTOBER, 1901) == 31

    def test_days_nov(self):
        assert Date.get_days_in_month(Date.NOVEMBER, 1901) == 30

    def test_days_dec(self):
        assert Date.get_days_in_month(Date.DECEMBER, 1901) == 31

    #####################
    # Repr
    #####################

    def test_repr_year_only(self):
        date = Date(year=1900)
        assert repr(date) == '??/??/1900'
        assert not date.day_set
        assert not date.month_set
        assert date.year_set

    def test_repr_month_only(self):
        date = Date(month=1)
        assert repr(date) == '??/01/????'
        assert not date.day_set
        assert date.month_set
        assert not date.year_set

    def test_repr_day_only(self):
        date = Date(day=1)
        assert repr(date) == '01/??/????'
        assert date.day_set
        assert not date.month_set
        assert not date.year_set

    def test_repr_month_year(self):
        date = Date(month=1, year=1900)
        assert repr(date) == '??/01/1900'
        assert not date.day_set
        assert date.month_set
        assert date.year_set

    def test_repr_day_year(self):
        date = Date(day=1, year=1900)
        assert repr(date) == '01/??/1900'
        assert date.day_set
        assert not date.month_set
        assert date.year_set

    def test_repr_day_month(self):
        date = Date(day=1, month=1)
        assert repr(date) == '01/01/????'
        assert date.day_set
        assert date.month_set
        assert not date.year_set

    def test_repr_all(self):
        date = Date(day=1, month=1, year=1900)
        assert repr(date) == '01/01/1900'
        assert date.day_set
        assert date.month_set
        assert date.year_set

    def test_repr_before(self):
        date = Date(day=1, month=Date.JANUARY, year=1900, precision=Date.BEFORE)
        assert repr(date) == '< 01/01/1900'

    def test_repr_after(self):
        date = Date(day=1, month=Date.JANUARY, year=1900, precision=Date.AFTER)
        assert repr(date) == '> 01/01/1900'

    def test_repr_circa(self):
        date = Date(day=1, month=Date.JANUARY, year=1900, precision=Date.APPROX)
        assert repr(date) == '~ 01/01/1900'

    #####################
    # Precision
    #####################

    def test_precision_invalid(self):
        with pytest.raises(ValueError):
            Date(year=1900, precision=-1)

    def test_precision(self):
        for p in Date.PRECISIONS:
            try:
                date = Date(year=1900, precision=p)
                assert date.precision == p
            except ValueError:
                raise AssertionError(f'Unrecognized precision <{p}>.')

    #####################
    # Validation
    #####################

    # Months

    def test_month_invalid_under(self):
        with pytest.raises(ValueError):
            Date(month=0)

    def test_month_invalid_over(self):
        with pytest.raises(ValueError):
            Date(month=13)

    # Days

    def test_day_invalid_under_1(self):
        with pytest.raises(ValueError):
            Date(day=0)

    def test_day_invalid_over_31(self):
        with pytest.raises(ValueError):
            Date(day=32)

    def test_days_invalid_jan(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.JANUARY)

    def test_days_invalid_mar(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.MARCH)

    def test_days_invalid_apr(self):
        with pytest.raises(ValueError):
            Date(day=31, month=Date.APRIL)

    def test_days_invalid_may(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.MAY)

    def test_days_invalid_jun(self):
        with pytest.raises(ValueError):
            Date(day=31, month=Date.JUNE)

    def test_days_invalid_jul(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.JULY)

    def test_days_invalid_aug(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.AUGUST)

    def test_days_invalid_sep(self):
        with pytest.raises(ValueError):
            Date(day=31, month=Date.SEPTEMBER)

    def test_days_invalid_oct(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.OCTOBER)

    def test_days_invalid_nov(self):
        with pytest.raises(ValueError):
            Date(day=31, month=Date.NOVEMBER)

    def test_days_invalid_dec(self):
        with pytest.raises(ValueError):
            Date(day=32, month=Date.DECEMBER)

    def test_days_invalid_feb(self):
        with pytest.raises(ValueError):
            Date(day=29, month=Date.FEBRUARY, year=1995)

    def test_days_invalid_feb_100_not_400(self):
        with pytest.raises(ValueError):
            Date(day=29, month=Date.FEBRUARY, year=1800)

    def test_days_valid_feb_29_no_year(self):
        Date(day=29, month=Date.FEBRUARY)
        with pytest.raises(ValueError):
            Date(day=30, month=Date.FEBRUARY)

    def test_days_valid_feb_leap_year_4(self):
        Date(day=29, month=Date.FEBRUARY, year=2008)
        with pytest.raises(ValueError):
            Date(day=30, month=Date.FEBRUARY, year=2008)

    def test_days_valid_feb_leap_year_400(self):
        Date(day=29, month=Date.FEBRUARY, year=2000)
        with pytest.raises(ValueError):
            Date(day=30, month=Date.FEBRUARY, year=2000)

    #####################
    # Operations
    #####################

    # Sum

    def test_add_year_year_only(self):
        assert Date(year=1905) + TimePeriod(years=1) == Date(year=1906)

    def test_add_years_year_only(self):
        assert Date(year=1905) + TimePeriod(years=2) == Date(year=1907)

    def test_add_months_no_days(self):
        assert Date(month=1, year=1905) + TimePeriod(months=2) == Date(month=3, year=1905)

    def test_add_months(self):
        assert Date(day=3, month=1, year=1905) + TimePeriod(months=2) == Date(day=3, month=3, year=1905)

    def test_add_month_jan_end(self):
        assert Date(day=31, month=1, year=1905) + TimePeriod(months=1) == Date(day=28, month=2, year=1905)

    def test_add_month_jan_end_leap_year(self):
        assert Date(day=31, month=1, year=2008) + TimePeriod(months=1) == Date(day=29, month=2, year=2008)

    def test_add_months_end_same_days_nb(self):
        assert Date(day=31, month=1, year=1905) + TimePeriod(months=2) == Date(day=31, month=3, year=1905)

    def test_add_month_end_different_days_nb(self):
        assert Date(day=31, month=3, year=1905) + TimePeriod(months=1) == Date(day=30, month=4, year=1905)

    def test_add_month_end_year_no_days(self):
        assert Date(month=12, year=1905) + TimePeriod(months=1) == Date(month=1, year=1906)

    def test_add_months_end_year_no_days(self):
        assert Date(month=12, year=1905) + TimePeriod(months=12) == Date(month=12, year=1906)

    def test_add_months_end_year2_no_days(self):
        assert Date(month=12, year=1905) + TimePeriod(months=24) == Date(month=12, year=1907)

    def test_add_month_end_year(self):
        assert Date(day=1, month=12, year=1905) + TimePeriod(months=1) == Date(day=1, month=1, year=1906)

    def test_add_months_end_year(self):
        assert Date(day=31, month=12, year=1905) + TimePeriod(months=2) == Date(day=28, month=2, year=1906)

    def test_add_day(self):
        assert Date(day=1, month=1, year=1905) + TimePeriod(days=1) == Date(day=2, month=1, year=1905)

    def test_add_day_end_month(self):
        assert Date(day=31, month=1, year=1905) + TimePeriod(days=1) == Date(day=1, month=2, year=1905)

    def test_add_day_end_year(self):
        assert Date(day=31, month=12, year=1905) + TimePeriod(days=1) == Date(day=1, month=1, year=1906)

    def test_add_days_next_month(self):
        assert Date(day=1, month=1, year=1905) + TimePeriod(days=31) == Date(day=1, month=2, year=1905)

    def test_add_days_feb(self):
        assert Date(day=1, month=2, year=1905) + TimePeriod(days=29) == Date(day=2, month=3, year=1905)

    def test_add_days_feb_leap_year(self):
        assert Date(day=1, month=2, year=2008) + TimePeriod(days=29) == Date(day=1, month=3, year=2008)

    def test_add_days_several_years(self):
        assert Date(day=1, month=1, year=1905) + TimePeriod(days=3000) == Date(day=20, month=3, year=1913)

    def test_add_month_and_day_month_end(self):
        assert Date(day=31, month=3, year=1905) + TimePeriod(days=1, months=1) == Date(day=1, month=5, year=1905)

    def test_add_year_only_precision_kept(self):
        assert Date(year=1905, precision=Date.APPROX) + TimePeriod(years=1) == Date(year=1906, precision=Date.APPROX)

    def test_add_month_year_precision_kept(self):
        assert Date(month=1, year=1905, precision=Date.APPROX) + TimePeriod(years=1) == \
               Date(month=1, year=1906, precision=Date.APPROX)

    def test_add_precision_kept(self):
        assert Date(day=1, month=1, year=1905, precision=Date.APPROX) + TimePeriod(years=1) == \
               Date(day=1, month=1, year=1906, precision=Date.APPROX)

    # Sum with negative TimePeriod

    def test_neg_add_year_year_only(self):
        assert Date(year=1905) + TimePeriod(years=-1) == Date(year=1904)

    def test_neg_add_years_year_only(self):
        assert Date(year=1905) + TimePeriod(years=-2) == Date(year=1903)

    def test_neg_add_months_no_days(self):
        assert Date(month=3, year=1905) + TimePeriod(months=-2) == Date(month=1, year=1905)

    def test_neg_add_months(self):
        assert Date(day=1, month=3, year=1905) + TimePeriod(months=-2) == Date(day=1, month=1, year=1905)

    def test_neg_add_month_mar_end(self):
        assert Date(day=31, month=3, year=1905) + TimePeriod(months=-1) == Date(day=28, month=2, year=1905)

    def test_neg_add_month_mar_end_leap_year(self):
        assert Date(day=31, month=3, year=2008) + TimePeriod(months=-1) == Date(day=29, month=2, year=2008)

    def test_neg_add_months_end_same_days_nb(self):
        assert Date(day=31, month=3, year=1905) + TimePeriod(months=-2) == Date(day=31, month=1, year=1905)

    def test_neg_add_month_end_different_days_nb(self):
        assert Date(day=31, month=5, year=1905) + TimePeriod(months=-1) == Date(day=30, month=4, year=1905)

    def test_neg_add_month_start_year_no_days(self):
        assert Date(month=1, year=1905) + TimePeriod(months=-1) == Date(month=12, year=1904)

    def test_neg_add_months_start_year_no_days(self):
        assert Date(month=1, year=1905) + TimePeriod(months=-12) == Date(month=1, year=1904)

    def test_neg_add_months_start_year2_no_days(self):
        assert Date(month=1, year=1905) + TimePeriod(months=-24) == Date(month=1, year=1903)

    def test_neg_add_month_start_year(self):
        assert Date(day=1, month=1, year=1905) + TimePeriod(months=-1) == Date(day=1, month=12, year=1904)

    def test_neg_add_months_start_year(self):
        assert Date(day=31, month=1, year=1905) + TimePeriod(months=-2) == Date(day=30, month=11, year=1904)

    def test_neg_add_day(self):
        assert Date(day=2, month=1, year=1905) + TimePeriod(days=-1) == Date(day=1, month=1, year=1905)

    def test_neg_add_day_start_month(self):
        assert Date(day=1, month=2, year=1905) + TimePeriod(days=-1) == Date(day=31, month=1, year=1905)

    def test_neg_add_day_start_year(self):
        assert Date(day=1, month=1, year=1905) + TimePeriod(days=-1) == Date(day=31, month=12, year=1904)

    def test_neg_add_days_previous_month(self):
        assert Date(day=1, month=5, year=1905) + TimePeriod(days=-3) == Date(day=28, month=4, year=1905)

    def test_neg_add_days_feb(self):
        assert Date(day=1, month=3, year=1905) + TimePeriod(days=-29) == Date(day=31, month=1, year=1905)

    def test_neg_add_days_feb_leap_year(self):
        assert Date(day=1, month=3, year=2008) + TimePeriod(days=-29) == Date(day=1, month=2, year=2008)

    def test_neg_add_days_several_years(self):
        assert Date(day=31, month=12, year=1905) + TimePeriod(days=-3000) == Date(day=13, month=10, year=1897)

    def test_neg_add_month_and_day_month_start(self):
        assert Date(day=1, month=5, year=1905) + TimePeriod(days=-1, months=-1) == Date(day=31, month=3, year=1905)

    def test_neg_add_year_only_precision_kept(self):
        assert Date(year=1905, precision=Date.APPROX) + TimePeriod(years=-1) == Date(year=1904, precision=Date.APPROX)

    def test_neg_add_month_year_precision_kept(self):
        assert Date(month=1, year=1905, precision=Date.APPROX) + TimePeriod(years=-1) == \
               Date(month=1, year=1904, precision=Date.APPROX)

    def test_neg_add_precision_kept(self):
        assert Date(day=1, month=1, year=1905, precision=Date.APPROX) + TimePeriod(years=-1) == \
               Date(day=1, month=1, year=1904, precision=Date.APPROX)

    def test_sub_is_add_neg(self):
        assert Date(month=1, year=1905, precision=Date.APPROX) + TimePeriod(years=-1) == \
               Date(month=1, year=1905, precision=Date.APPROX) - TimePeriod(years=1)

    # Difference

    def test_sub_year_only(self):
        assert Date(year=1906) - Date(year=1905) == TimePeriod(years=1)

    def test_sub_month_only_error(self):
        with pytest.raises(ValueError):
            Date(month=2) - Date(month=1)

    def test_sub_partial_year_error(self):
        with pytest.raises(ValueError):
            Date(month=2, year=2) - Date(month=1)

    def test_sub_day_only_error(self):
        with pytest.raises(ValueError):
            Date(day=2) - Date(day=1)

    def test_sub_day_month_error(self):
        with pytest.raises(ValueError):
            Date(day=2, month=2) - Date(day=1, month=1)

    def test_sub_partial_month(self):
        assert Date(month=1, year=1906) - Date(year=1905) == TimePeriod(years=1)
        assert Date(year=1906) - Date(month=1, year=1905) == TimePeriod(years=1)

    def test_sub_partial_day(self):
        assert Date(day=1, month=2, year=1906) - Date(month=1, year=1905) == TimePeriod(months=1, years=1)
        assert Date(month=2, year=1906) - Date(day=1, month=1, year=1905) == TimePeriod(months=1, years=1)

    def test_sub_day_partial_month(self):
        assert Date(day=2, month=1, year=1906) - Date(day=1, year=1905) == TimePeriod(years=1)
        assert Date(day=2, year=1906) - Date(day=1, month=1, year=1905) == TimePeriod(years=1)

    def test_sub_same_month_diff_year(self):
        assert Date(month=1, year=1906) - Date(month=1, year=1905) == TimePeriod(years=1)

    def test_sub_diff_month_diff_year(self):
        assert Date(month=2, year=1906) - Date(month=1, year=1905) == TimePeriod(months=1, years=1)

    def test_sub_same_day_diff_month_diff_year(self):
        assert Date(day=1, month=2, year=1906) - Date(day=1, month=1, year=1905) == TimePeriod(months=1, years=1)

    def test_sub_diff_day_diff_month_diff_year(self):
        assert Date(day=2, month=2, year=1906) - Date(day=1, month=1, year=1905) == \
               TimePeriod(days=1, months=1, years=1)

    def test_sub_neg(self):
        assert Date(day=1, month=1, year=1905) - Date(day=2, month=2, year=1906) == \
               TimePeriod(days=-1, months=-1, years=-1)

    def test_sub_before1(self):
        with pytest.raises(ValueError):
            Date(year=2, precision=Date.BEFORE) - Date(year=1)

    def test_sub_before2(self):
        with pytest.raises(ValueError):
            Date(year=2) - Date(year=1, precision=Date.BEFORE)

    def test_sub_after1(self):
        with pytest.raises(ValueError):
            Date(year=2, precision=Date.AFTER) - Date(year=1)

    def test_sub_after2(self):
        with pytest.raises(ValueError):
            Date(year=2) - Date(year=1, precision=Date.AFTER)

    #####################
    # Comparison
    #####################

    # eq

    def test_compare_eq_year_only(self):
        assert Date(year=1905) == Date(year=1905)

    def test_compare_eq_month_only(self):
        assert Date(month=1) == Date(month=1)

    def test_compare_eq_day_only(self):
        assert Date(day=1) == Date(day=1)

    def test_compare_eq_no_year(self):
        assert Date(day=1, month=1) == Date(day=1, month=1)

    def test_compare_eq_no_month(self):
        assert Date(day=1, year=1905) == Date(day=1, year=1905)

    def test_compare_eq_no_day(self):
        assert Date(month=1, year=1905) == Date(month=1, year=1905)

    def test_compare_eq_full(self):
        assert Date(day=1, month=1, year=1905) == Date(day=1, month=1, year=1905)

    # neq

    def test_compare_neq_year_only(self):
        assert Date(year=1905) != Date(year=1906)

    def test_compare_neq_month_only(self):
        assert Date(month=1) != Date(month=2)

    def test_compare_neq_day_only(self):
        assert Date(day=1) != Date(day=2)

    def test_compare_neq_no_days_diff_month_same_year(self):
        assert Date(month=1, year=1905) != Date(month=2, year=1905)

    def test_compare_neq_no_days_same_month_diff_year(self):
        assert Date(month=1, year=1905) != Date(month=1, year=1906)

    def test_compare_neq_diff_day_no_month_same_year(self):
        assert Date(day=1, year=1905) != Date(day=2, year=1905)

    def test_compare_neq_same_day_no_month_diff_year(self):
        assert Date(day=1, year=1905) != Date(day=1, year=1906)

    def test_compare_neq_diff_day_same_month_no_year(self):
        assert Date(day=1, month=1) != Date(day=2, month=1)

    def test_compare_neq_same_day_diff_month_no_year(self):
        assert Date(day=1, month=1) != Date(day=1, month=2)

    def test_compare_neq_partial_day_same_month_same_year(self):
        assert Date(day=1, month=1, year=1905) != Date(month=1, year=1905)
        assert Date(month=1, year=1905) != Date(day=1, month=1, year=1905)

    def test_compare_neq_same_day_partial_month_same_year(self):
        assert Date(day=1, month=1, year=1905) != Date(day=1, year=1905)
        assert Date(day=1, year=1905) != Date(day=1, month=1, year=1905)

    def test_compare_neq_same_day_same_month_partial_year(self):
        assert Date(day=1, month=1, year=1905) != Date(day=1, month=1)
        assert Date(day=1, month=1) != Date(day=1, month=1, year=1905)

    def test_compare_neq_partial_day_diff_month_same_year(self):
        assert Date(day=1, month=1, year=1905) != Date(month=2, year=1905)
        assert Date(month=1, year=1905) != Date(day=1, month=2, year=1905)

    def test_compare_neq_partial_day_same_month_diff_year(self):
        assert Date(day=1, month=1, year=1905) != Date(month=1, year=1906)
        assert Date(month=1, year=1905) != Date(day=1, month=1, year=1906)

    def test_compare_neq_diff_day_partial_month_same_year(self):
        assert Date(day=1, month=1, year=1905) != Date(day=2, year=1905)
        assert Date(day=1, year=1905) != Date(day=2, month=1, year=1905)

    def test_compare_neq_same_day_partial_month_diff_year(self):
        assert Date(day=1, month=1, year=1905) != Date(day=1, year=1906)
        assert Date(day=1, year=1905) != Date(day=1, month=1, year=1906)

    def test_compare_neq_diff_day_same_month_partial_year(self):
        assert Date(day=1, month=1, year=1905) != Date(day=2, month=1)
        assert Date(day=1, month=1) != Date(day=2, month=1, year=1905)

    def test_compare_neq_same_day_diff_month_partial_year(self):
        assert Date(day=1, month=2, year=1905) != Date(day=1, month=1)
        assert Date(day=1, month=1) != Date(day=1, month=2, year=1905)

    def test_compare_neq_nothing_common(self):
        assert Date(month=1) != Date(day=1, year=1905)
        assert Date(day=1, year=1905) != Date(month=1)

    # gt

    def test_compare_gt_year_only(self):
        assert Date(year=1906) > Date(year=1905)

    def test_compare_gt_month_only(self):
        assert Date(month=2) > Date(month=1)

    def test_compare_gt_day_only(self):
        assert Date(day=2) > Date(day=1)

    def test_compare_gt_no_days_diff_month_same_year(self):
        assert Date(month=2, year=1905) > Date(month=1, year=1905)

    def test_compare_gt_no_days_same_month_diff_year(self):
        assert Date(month=1, year=1906) > Date(month=1, year=1905)

    def test_compare_gt_diff_days_no_month_same_year(self):
        assert Date(day=2, year=1905) > Date(day=1, year=1905)

    def test_compare_gt_same_days_no_month_diff_year(self):
        assert Date(day=1, year=1906) > Date(day=1, year=1905)

    def test_compare_gt_diff_days_same_month_no_year(self):
        assert Date(day=2, month=1) > Date(day=1, month=1)

    def test_compare_gt_same_days_diff_month_no_year(self):
        assert Date(day=1, month=2) > Date(day=1, month=1)

    def test_compare_gt_partial_day_diff_month_same_year(self):
        assert Date(day=1, month=2, year=1905) > Date(month=1, year=1905)
        assert Date(month=2, year=1905) > Date(day=1, month=1, year=1905)

    def test_compare_gt_partial_day_same_month_diff_year(self):
        assert Date(day=1, month=1, year=1906) > Date(month=1, year=1905)
        assert Date(month=1, year=1906) > Date(day=1, month=1, year=1905)

    def test_compare_gt_diff_day_no_month_same_year(self):
        assert Date(day=2, month=1, year=1905) > Date(day=1, year=1905)
        assert Date(day=2, year=1905) > Date(day=1, month=1, year=1905)

    def test_compare_gt_same_day_no_month_diff_year(self):
        assert Date(day=1, month=1, year=1906) > Date(day=1, year=1905)
        assert Date(day=1, year=1906) > Date(day=1, month=1, year=1905)

    def test_compare_gt_diff_day_same_month_no_year(self):
        assert Date(day=2, month=1, year=1905) > Date(day=1, month=1)
        assert Date(day=2, month=1) > Date(day=1, month=1, year=1905)

    def test_compare_gt_same_day_diff_month_no_year(self):
        assert Date(day=1, month=2, year=1906) > Date(day=1, month=1)
        assert Date(day=1, month=2) > Date(day=1, month=1, year=1905)
