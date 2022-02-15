


@classmethod
    def test_with_pyqt_slots(cls, outer_signals, pages: [SubjectPage] = None, test_key='test_result'):

        # set up pages for test
        if pages is None:
            try:
                pages_collection = cls.get_he_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                outer_signals.status.emit(0)
                outer_signals.finished.emit()
                outer_signals.error.emit(('error in loading pages, test is closed', 'nothing was checked'))
                raise e

        else:
            pages_collection = pages
        # set up session for test
        try:
            session = cls.get_sessions()
        except WebDriverException as e:
            print('error loading sessions, test is closed')
            outer_signals.status.emit(0)
            outer_signals.error.emit(('error loading sessions, test is closed', 'nothing was checked'))
            outer_signals.finished.emit()
            raise e
        except Exception as e:
            print('error loading sessions, test is closed')
            outer_signals.status.emit(0)
            outer_signals.error.emit(('error loading sessions, test is closed', 'nothing was checked'))
            outer_signals.finished.emit()
            raise e
        # status flow
        outer_signals.monitor_data.emit('initializing test environment...')
        print('initializing test environment..')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        outer_signals.monitor_data.emit('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))

        error_pages = []
        pages_size = len(pages_collection)
        print('num pages', str(len(pages_collection)))
        outer_signals.monitor_data.emit('num pages: ' + str(pages_size))
        # set summery object

        summary = []
        summary.append(datetime.date.today().strftime('%d.%m.%y'))  # date
        summary.append(str(current_time))  # test start time
        summary.append(str(pages_size))  # number of chosen pages for test
        summary.append(0)  # counter for checked pages
        summary.append(0)  # counter for error pages
        try:
            for i, page in enumerate(pages_collection):
                if not outer_signals.end_flag.empty():
                    outer_signals.monitor_data.emit('test canceled')
                    return

                percents = (float(i + 1) / pages_size) * 100
                outer_signals.status.emit(percents * 100)
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)

                # executor_url = session.command_executor._url
                # session_id = session.session_id
                # load page
                timeout = 5
                try:
                    main_element = WebDriverWait(session, 10).until(
                        EC.presence_of_element_located((By.XPATH, ROOT_ELEMENT))
                    )

                    # start = time.time()
                    cls.testPage(page, main_element)
                    # print('average page test time: {}'.format(str(time.time()-start)))
                    percents = (float(i + 1) / pages_size) * 100
                    outer_signals.status.emit(percents)
                except StaleElementReferenceException:
                    try:
                        main_element = WebDriverWait(session, timeout).until(
                            expected_conditions.presence_of_element_located(
                                (By.XPATH, "//body[@class='INDDesktop INDChrome INDlangdirRTL INDpositionRight']")))
                        cls.testPage(page, main_element)

                    except Exception:
                        page.stats_part.errors.append('unknown error')
                        break
                except TimeoutException:
                    print("Timed out waiting for page to load: {}".format(page.name))
                    DataBase.save_test_result(test_, page)
                    continue
                except NoSuchWindowException:
                    page.stats_part.errors.append("couldn't find root element")
                    page.isChecked = False
                    DataBase.save_test_result(test_key, page)
                    continue
                summary[3] += 1
                if len(page.get_errors()) > 0:
                    # print(page.name, page.link.url)
                    print(page.error_to_str())
                    outer_signals.page_info.emit(str({'name': page.name, 'url': page.link.url, 'error': True}))
                    outer_signals.monitor_data.emit(str(page.error_to_str().replace('\n', '<br>')))
                    error_pages.append((page.name, page.link.url, page.error_to_str()))
                    DataBase.save_test_result(test_key, page)
                    summary[4] += 1
                else:
                    outer_signals.page_info.emit(str({'name': page.name, 'url': page.link.url, 'error': False}))
                    # outer_signals.monitor_data.emit(str(200))
        except NoSuchWindowException as e:
            print('Main test stopped due to unexpected  session close')
            outer_signals.monitor_data.emit('Main test stopped due to unexpected  session close')
            outer_signals.finished.emit()
            raise e
        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            outer_signals.monitor_data.emit('main process stopped due to exception: ' + str(e))
            outer_signals.finished.emit()
            raise e
        finally:
            session.close()
            outer_signals.finished.emit()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)
            outer_signals.monitor_data.emit('test ended on: ' + current_time)
            DataBase.save_test_result(test_key, page)
            DataBase.save_summary_result(test_key, summary)