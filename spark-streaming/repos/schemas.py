from pyspark.sql.types import ArrayType, BooleanType, IntegerType, StringType, StructField, StructType, TimestampType

commits_schema = StructType([
    StructField("_id", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("copyingData", BooleanType(), True)
    ])),
    StructField("operationType", StringType(), True),
    StructField("documentKey", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ]))
    ])),
    StructField("fullDocument", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("sha", StringType(), True),
        StructField("commit", StructType([
            StructField("author", StructType([
                StructField("name", StringType(), True),
                StructField("email", StringType(), True),
                StructField("date", TimestampType(), True)
            ])),
            StructField("committer", StructType([
                StructField("name", StringType(), True),
                StructField("email", StringType(), True),
                StructField("date", TimestampType(), True)
            ])),
            StructField("message", StringType(), True),
            StructField("tree", StructType([
                StructField("sha", StringType(), True),
                StructField("url", StringType(), True)
            ])),
            StructField("url", StringType(), True),
            StructField("comment_count", IntegerType(), True),
        ])),
        StructField("url", StringType(), True),
        StructField("html_url", StringType(), True),
        StructField("comments_url", StringType(), True),
        StructField("author", StructType([
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("avatar_url", StringType(), True),
            StructField("gravatar_url", StringType(), True),
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("followers_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True)
        ])),
        StructField("committer", StructType([
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("avatar_url", StringType(), True),
            StructField("gravatar_url", StringType(), True),
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("followers_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True)
        ])),
        StructField("parents", ArrayType(
            StructType([
                StructField("sha", StringType(), True),
                StructField("url", StringType(), True),
                StructField("html_url", StringType(), True)
            ])
        )),
        StructField("stats", StructType([
            StructField("total", IntegerType(), True),
            StructField("additions", IntegerType(), True),
            StructField("deletions", IntegerType(), True)
        ])),
        StructField("files", ArrayType(
            StructType([
                StructField("sha", StringType(), True),
                StructField("filename", StringType(), True),
                StructField("status", StringType(), True),
                StructField("additions", IntegerType(), True),
                StructField("deletions", IntegerType(), True),
                StructField("changes", IntegerType(), True),
                StructField("blob_url", StringType(), True),
                StructField("raw_url", StringType(), True),
                StructField("content_url", StringType(), True),
                StructField("patch", StringType(), True)
            ])
        ))
    ]))
])

repos_schema = StructType([
    StructField("_id", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("copyingData", BooleanType(), True)
    ])),
    StructField("operationType", StringType(), True),
    StructField("documentKey", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ]))
    ])),
    StructField("fullDocument", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("full_name", StringType(), True),
        StructField("Owner", StructType([
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("gravatar_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True)
        ])),
        StructField("private", BooleanType(), True),
        StructField("html_url", StringType(), True),
        StructField("description", StringType(), True),
        StructField("fork", BooleanType(), True),
        StructField("url", StringType(), True),
        StructField("forks_url", StringType(), True),
        StructField("collaborators_url", StringType(), True),
        StructField("teams_url", StringType(), True),
        StructField("hooks_url", StringType(), True),
        StructField("issue_events_url", StringType(), True),
        StructField("events_url", StringType(), True),
        StructField("assignees_url", StringType(), True),
        StructField("branches_url", StringType(), True),
        StructField("tags_url", StringType(), True),
        StructField("blobs_url", StringType(), True),
        StructField("git_tags_url", StringType(), True),
        StructField("git_refs_url", StringType(), True),
        StructField("trees_url", StringType(), True),
        StructField("statuses_url", StringType(), True),
        StructField("languages_url", StringType(), True),
        StructField("stargazers_url", StringType(), True),
        StructField("contributors_url", StringType(), True),
        StructField("subscribers_url", StringType(), True),
        StructField("subscription_url", StringType(), True),
        StructField("commits_url", StringType(), True),
        StructField("git_commits_url", StringType(), True),
        StructField("comments_url", StringType(), True),
        StructField("issue_comment_url", StringType(), True),
        StructField("contents_url", StringType(), True),
        StructField("compare_url", StringType(), True),
        StructField("merges_url", StringType(), True),
        StructField("archive_url", StringType(), True),
        StructField("downloads_url", StringType(), True),
        StructField("issues_url", StringType(), True),
        StructField("pulls_url", StringType(), True),
        StructField("milestones_url", StringType(), True),
        StructField("notifications_url", StringType(), True),
        StructField("labels_url", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
        StructField("pushed_at", TimestampType(), True),
        StructField("git_url", StringType(), True),
        StructField("ssh_url", StringType(), True),
        StructField("clone_url", StringType(), True),
        StructField("svn_url", StringType(), True),
        StructField("homepage", StringType(), True),
        StructField("size", IntegerType(), True),
        StructField("watchers_count", IntegerType(), True),
        StructField("language", StringType(), True),
        StructField("has_issues", BooleanType(), True),
        StructField("has_downloads", BooleanType(), True),
        StructField("has_wiki", BooleanType(), True),
        StructField("forks_count", IntegerType(), True),
        StructField("mirror_url", StringType(), True),
        StructField("open_issues_count", IntegerType(), True),
        StructField("forks", IntegerType(), True),
        StructField("open_issues", IntegerType(), True),
        StructField("watchers", IntegerType(), True),
        StructField("master_branch", StringType(), True),
        StructField("default_branch", StringType(), True),
        StructField("permissions", StructType([
            StructField("admin", BooleanType(), True),
            StructField("push", BooleanType(), True),
            StructField("pull", BooleanType(), True),
        ])),
        StructField("network_count", IntegerType(), True),
        StructField("parent", StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("owner", StructType([
                StructField("login", StringType(), True),
                StructField("id", IntegerType(), True),
                StructField("avatar_url", StringType(), True),
                StructField("gravatar_url", StringType(), True),
                StructField("url", StringType(), True),
                StructField("html_url", StringType(), True),
                StructField("followers_url", StringType(), True),
                StructField("following_url", StringType(), True),
                StructField("gists_url", StringType(), True),
                StructField("starred_url", StringType(), True),
                StructField("subscriptions_url", StringType(), True),
                StructField("organizations_url", StringType(), True),
                StructField("repos_url", StringType(), True),
                StructField("events_url", StringType(), True),
                StructField("received_events_url", StringType(), True),
                StructField("type", StringType(), True)
            ])),
            StructField("private", BooleanType(), True),
            StructField("html_url", StringType(), True),
            StructField("description", StringType(), True),
            StructField("fork", BooleanType(), True),
            StructField("url", StringType(), True),
            StructField("forks_url", StringType(), True),
            StructField("keys_url", StringType(), True),
            StructField("collaborators_url", StringType(), True),
            StructField("teams_url", StringType(), True),
            StructField("hooks_url", StringType(), True),
            StructField("issue_events_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("assignees_url", StringType(), True),
            StructField("branches_url", StringType(), True),
            StructField("tags_url", StringType(), True),
            StructField("blobs_url", StringType(), True),
            StructField("git_tags_url", StringType(), True),
            StructField("git_refs_url", StringType(), True),
            StructField("trees_url", StringType(), True),
            StructField("statuses_url", StringType(), True),
            StructField("languages_url", StringType(), True),
            StructField("stargazers_url", StringType(), True),
            StructField("contributors_url", StringType(), True),
            StructField("subscribers_url", StringType(), True),
            StructField("subscription_url", StringType(), True),
            StructField("commits_url", StringType(), True),
            StructField("git_commits_url", StringType(), True),
            StructField("comments_url", StringType(), True),
            StructField("issue_comment_url", StringType(), True),
            StructField("contents_url", StringType(), True),
            StructField("compare_url", StringType(), True),
            StructField("merges_url", StringType(), True),
            StructField("archive_url", StringType(), True),
            StructField("downloads_url", StringType(), True),
            StructField("issues_url", StringType(), True),
            StructField("pulls_url", StringType(), True),
            StructField("milestones_url", StringType(), True),
            StructField("notifications_url", StringType(), True),
            StructField("labels_url", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True),
            StructField("pushed_at", TimestampType(), True),
            StructField("git_url", StringType(), True),
            StructField("ssh_url", StringType(), True),
            StructField("clone_url", StringType(), True),
            StructField("svn_url", StringType(), True),
            StructField("homepage", StringType(), True),
            StructField("size", IntegerType(), True),
            StructField("watchers_count", IntegerType(), True),
            StructField("language", StringType(), True),
            StructField("has_issues", BooleanType(), True),
            StructField("has_downloads", BooleanType(), True),
            StructField("has_wiki", BooleanType(), True),
            StructField("forks_count", IntegerType(), True),
            StructField("mirror_url", StringType(), True),
            StructField("open_issues_count", IntegerType(), True),
            StructField("forks", IntegerType(), True),
            StructField("open_issues", IntegerType(), True),
            StructField("watchers", IntegerType(), True),
            StructField("master_branch", StringType(), True),
            StructField("default_branch", StringType(), True),
        ])),
        StructField("source", StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("full_name", StringType(), True),
            StructField("owner", StructType([
                StructField("login", StringType(), True),
                StructField("id", IntegerType(), True),
                StructField("avatar_url", StringType(), True),
                StructField("gravatar_url", StringType(), True),
                StructField("url", StringType(), True),
                StructField("html_url", StringType(), True),
                StructField("followers_url", StringType(), True),
                StructField("following_url", StringType(), True),
                StructField("gists_url", StringType(), True),
                StructField("starred_url", StringType(), True),
                StructField("subscriptions_url", StringType(), True),
                StructField("organizations_url", StringType(), True),
                StructField("repos_url", StringType(), True),
                StructField("events_url", StringType(), True),
                StructField("received_events_url", StringType(), True),
                StructField("type", StringType(), True)
            ])),
            StructField("private", BooleanType(), True),
            StructField("html_url", StringType(), True),
            StructField("description", StringType(), True),
            StructField("fork", BooleanType(), True),
            StructField("url", StringType(), True),
            StructField("forks_url", StringType(), True),
            StructField("keys_url", StringType(), True),
            StructField("collaborators_url", StringType(), True),
            StructField("teams_url", StringType(), True),
            StructField("hooks_url", StringType(), True),
            StructField("issue_events_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("assignees_url", StringType(), True),
            StructField("branches_url", StringType(), True),
            StructField("tags_url", StringType(), True),
            StructField("blobs_url", StringType(), True),
            StructField("git_tags_url", StringType(), True),
            StructField("git_refs_url", StringType(), True),
            StructField("trees_url", StringType(), True),
            StructField("statuses_url", StringType(), True),
            StructField("languages_url", StringType(), True),
            StructField("stargazers_url", StringType(), True),
            StructField("contributors_url", StringType(), True),
            StructField("subscribers_url", StringType(), True),
            StructField("subscription_url", StringType(), True),
            StructField("commits_url", StringType(), True),
            StructField("git_commits_url", StringType(), True),
            StructField("comments_url", StringType(), True),
            StructField("issue_comment_url", StringType(), True),
            StructField("contents_url", StringType(), True),
            StructField("compare_url", StringType(), True),
            StructField("merges_url", StringType(), True),
            StructField("archive_url", StringType(), True),
            StructField("downloads_url", StringType(), True),
            StructField("issues_url", StringType(), True),
            StructField("pulls_url", StringType(), True),
            StructField("milestones_url", StringType(), True),
            StructField("notifications_url", StringType(), True),
            StructField("labels_url", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True),
            StructField("pushed_at", TimestampType(), True),
            StructField("git_url", StringType(), True),
            StructField("ssh_url", StringType(), True),
            StructField("clone_url", StringType(), True),
            StructField("svn_url", StringType(), True),
            StructField("homepage", StringType(), True),
            StructField("size", IntegerType(), True),
            StructField("watchers_count", IntegerType(), True),
            StructField("language", StringType(), True),
            StructField("has_issues", BooleanType(), True),
            StructField("has_downloads", BooleanType(), True),
            StructField("has_wiki", BooleanType(), True),
            StructField("forks_count", IntegerType(), True),
            StructField("mirror_url", StringType(), True),
            StructField("open_issues_count", IntegerType(), True),
            StructField("forks", IntegerType(), True),
            StructField("open_issues", IntegerType(), True),
            StructField("watchers", IntegerType(), True),
            StructField("master_branch", StringType(), True),
            StructField("default_branch", StringType(), True)
        ]))
    ]))
])
