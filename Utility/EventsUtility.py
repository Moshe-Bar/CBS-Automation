


@classmethod
    def test_with_events(cls, working: threading.Event(), shared_data: Queue = Queue(),
                         progress_status: Queue = Queue(),
                         pages=None):
        # set up pages for test
        if pages is None:
            try:
                pages_collection = cls.get_he_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                shared_data.put('error in loading pages, test is closed')
                working.clear()
                raise e
        else:
            pages_collection = pages
        # set up session for test
        try:
            session = cls.get_sessions()  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            shared_data.put('error loading sessions, test is closed')
            working.clear()
            raise e
        # status flow
        shared_data.put('initializing test environment...')
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        shared_data.put('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))

        error_pages = []
        pages_size = len(pages_collection)
        print('num pages', str(len(pages_collection)))
        shared_data.put('num pages: ' + str(pages_size))

        try:
            for i, page in enumerate(pages_collection):
                if not working.isSet():
                    raise Exception('test canceled')
                    # outside canceled

                percents = i / pages_size
                progress_status.put(percents)
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)
                cls.testPage(page, session)

                if len(page.stats_part.errors) > 0:
                    print(page.name, page.link.url)
                    print(page.stats_part.errors)
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(page.stats_part.errors)
                    error_pages.append((page.name, page.link.url, page.stats_part.errors))
                else:
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(str(200))

        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            shared_data.put('main process stopped due to exception: ' + str(e))
            # end_flag.put('main process stopped due to exception: ' + str(e))
            working.clear()
        finally:
            session.close()
            # end_flag.put('end main process')
            if working.isSet():
                working.clear()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)
            shared_data.put('test ended on: ' + current_time)